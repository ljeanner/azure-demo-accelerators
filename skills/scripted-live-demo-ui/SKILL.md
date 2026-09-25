---
name: scripted-live-demo-ui
description: "Build a scripted agent/chat UI that feels live: the user's message types itself character by character, the composer sends on its own, thinking steps cycle, and the assistant reply reveals progressively. USE FOR: fake a live demo, simulate typing, typewriter effect in a demo, scripted chat demo, make the demo look real, agent conversation demo, demo that runs on click, canned conversation UI, scripted scenario replay, suggested replies that auto-type, demo storyboard in a web app. DO NOT USE FOR: wiring a real LLM or streaming a real API response, generic UI animation work, or production chat features."
---

# Scripted "live demo" chat UI

Build a chat/agent interface that **looks like a real live session** but is fully scripted. The
presenter clicks one suggested reply and everything else plays by itself: the text types into the
composer, the message sends, the agent "thinks" through steps, and the answer reveals progressively.

No model call, no latency risk, no bad surprise on stage — but the room sees a live product.

Reference implementation: `zava-website/src/app/frontier/experience/page.tsx` in the Zava demo, and
<https://github.com/ljeanner/azure-demo-accelerators>.

---

## Why scripted rather than real

| | Scripted | Real model call |
|---|---|---|
| Latency | Chosen, constant | Variable, sometimes 30 s |
| Answer | Identical every rehearsal | Drifts between runs |
| Offline / bad wifi | Works | Dead demo |
| Credibility | High **if the timings are right** | High |

The whole craft is in the timings. Get them wrong and it reads as a video; get them right and people
ask for the URL.

---

## The five-beat loop

Every turn follows the same beats. Respect the order and the pauses.

```
click suggested reply
  → 1. type into composer        ~32 ms per character
  → 2. pause, then send          ~600 ms
  → 3. thinking steps            ~1400 ms per step
  → 4. reveal the answer         ~110 ticks of 45 ms, whatever the length
  → 5. pause, commit, advance    ~500 ms
```

Two non-obvious details that make it feel real:

- **Reveal by chunks, not by characters.** Compute `step = max(1, round(length / 110))` and append
  `step` characters per tick. A long answer then takes the same time as a short one — which is what
  a streaming model actually looks like, and it stops a 900-character answer from taking 40 seconds.
- **Type the user message one character at a time** (fixed 32 ms). Human typing is *not* chunked,
  and this is the beat the audience subconsciously checks.

---

## Data model

Script the conversation as a flat array of scenes. One scene = one turn. Keep the script in a
separate file from the component — you will edit it far more often than the UI.

```ts
type ThinkingStep = {
  label: string;               // "Querying Fabric"
  sub: string;                 // "Aggregating weekly sales for the Garden category."
};

type Choice = {
  label: string;               // text on the suggested-reply button
  user: string;                // what types itself into the composer
  assistant: string;           // the answer that reveals
  chain: string;               // attribution line: "Fabric data agent • OneLake"
  thinkingSteps?: ThinkingStep[];
  mention?: string;            // types "@Agent " first, with a picker
  proactive?: boolean;         // no user message: plays as a system notification
  autoTriggerOnly?: boolean;   // not offered as a button; fired from inside a card
  chainNext?: boolean;         // auto-continue into the next scene when done
  card?: unknown;              // any rich payload rendered under the text
};

type Scene = { choices: Choice[] };
```

Offering **two or three choices per scene** is what sells it: the audience sees a branch, so it does
not look like a single linear recording — even if every branch reconverges on the next scene.

---

## Implementation

### State and timers

```tsx
const [messages, setMessages] = useState<Message[]>([]);
const [draftText, setDraftText] = useState("");
const [isTyping, setIsTyping] = useState(false);
const [processingStep, setProcessingStep] = useState<ThinkingStep | null>(null);
const [isAssistantTyping, setIsAssistantTyping] = useState(false);
const [assistantDraft, setAssistantDraft] = useState("");
const [sceneIndex, setSceneIndex] = useState(0);

// Mirrors sceneIndex synchronously. Chained steps schedule the next hop inside a
// setTimeout closure, where the `sceneIndex` state variable is stale and would
// replay the same scene forever. Always read the ref inside a timer.
const sceneIndexRef = useRef(0);

const typingRef = useRef<ReturnType<typeof setInterval> | null>(null);
const sendTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
const thinkingRef = useRef<ReturnType<typeof setInterval> | null>(null);
const assistantTypingRef = useRef<ReturnType<typeof setInterval> | null>(null);
const assistantPauseRef = useRef<ReturnType<typeof setTimeout> | null>(null);

// One guard for the whole loop: disables every button while a turn plays.
// Without it, an impatient presenter double-clicks and two scripts interleave.
const isBusy = isTyping || processingStep !== null || isAssistantTyping;
```

Always provide a single `clearAllTimers()` clearing every ref, call it at the start of each turn,
and register it on unmount:

```tsx
useEffect(() => clearAllTimers, []);
```

### Beat 1-2 — the composer types and sends itself

```tsx
const typeComposerText = (full: string, prefixLen: number) => {
  let i = prefixLen;
  typingRef.current = setInterval(() => {
    i += 1;
    if (i >= full.length) {
      clearInterval(typingRef.current!);
      typingRef.current = null;
      setDraftText(full);
      sendTimeoutRef.current = setTimeout(() => {
        const choice = pendingChoiceRef.current;
        if (!choice) return;
        commitUserMessage(choice);
        setIsTyping(false);
        setDraftText("");
        beginThinking(choice);
      }, 600);                 // the beat that reads as "she just hit Enter"
      return;
    }
    setDraftText(full.slice(0, i));
  }, 32);
};
```

Render a blinking caret next to `draftText` while `isTyping`, and keep the real `<input>` disabled so
nobody types over the script.

### Beat 3 — thinking steps

```tsx
const beginThinking = (choice: Choice) => {
  const steps = choice.thinkingSteps?.length
    ? choice.thinkingSteps
    : [{ label: `Consulting ${choice.chain}`, sub: "Retrieving the data needed to answer." }];
  let idx = 0;
  setProcessingStep(steps[0]);
  thinkingRef.current = setInterval(() => {
    idx += 1;
    if (idx >= steps.length) {
      clearInterval(thinkingRef.current!);
      thinkingRef.current = null;
      setProcessingStep(null);
      beginAssistantReveal(choice);
      return;
    }
    setProcessingStep(steps[idx]);
  }, 1400);
};
```

**This is where you narrate.** Two to four steps is the sweet spot: enough time to say "it is
translating the question into SQL over the lakehouse", short enough that nobody gets bored. Name real
systems in the labels — that is what makes the architecture legible without a slide.

### Beat 4-5 — the answer reveals

```tsx
const beginAssistantReveal = (choice: Choice) => {
  if (choice.card || !choice.assistant) {
    commitAssistantMessage(choice);   // structured cards appear fully formed
    return;
  }
  setIsAssistantTyping(true);
  setAssistantDraft("");
  const full = choice.assistant;
  let i = 0;
  const step = Math.max(1, Math.round(full.length / 110));
  assistantTypingRef.current = setInterval(() => {
    i += step;
    if (i >= full.length) {
      clearInterval(assistantTypingRef.current!);
      assistantTypingRef.current = null;
      setAssistantDraft(full);
      assistantPauseRef.current = setTimeout(() => {
        commitAssistantMessage(choice);
        setIsAssistantTyping(false);
        setAssistantDraft("");
      }, 500);
      return;
    }
    setAssistantDraft(full.slice(0, i));
  }, 45);
};
```

`commitAssistantMessage` appends the message, then advances **through the ref**:

```tsx
const nextIndex = sceneIndexRef.current + 1;
sceneIndexRef.current = nextIndex;
setSceneIndex(nextIndex);

if (choice.chainNext) {
  const next = scenes[nextIndex]?.choices.find((c) => c.autoTriggerOnly);
  if (next) scenarioAutoAdvanceRef.current = setTimeout(() => startTyping(next), 700);
}
```

---

## Effects worth adding

Add these only once the five-beat loop feels right.

- **Rich cards instead of text.** A table, a chart, an email draft, a contact card. Skip the reveal
  animation for them — a formatted report appearing progressively looks broken, not live. Gate on
  `if (choice.card) commitAssistantMessage(choice)`.
- **Interactive cards.** A Send button inside an email draft, an Approve/Reject pair. The presenter
  clicks it and the script continues from there instead of from a suggested reply — this is the
  moment the demo stops looking like a replay.
- **`@agent` mention.** On the first mention, type `@`, open a small agent picker for ~1800 ms, close
  it, then type the rest. It shows multi-agent routing in three seconds, with no explanation needed.
- **Proactive turns** (`proactive: true`). No user message: the agent speaks first, as a
  notification. Perfect for "an alert just fired". Chain two or three with `chainNext` to show
  agent-to-agent handoff.
- **Configurable identities.** Put the presenter's and approver's names in a small settings panel
  persisted in `localStorage`, and substitute tokens in the script at render time. A colleague can
  then reuse your demo with their own name in thirty seconds — this is what turns a demo into an asset.
- **One real side effect, opt-in.** Exactly one thing that is genuinely real (a real email, a real
  phone call) lands harder than ten simulated ones. Guard it behind configuration and fall back to
  simulation when unset, so the demo never breaks on someone else's laptop.

---

## Golden rules

- **Script in a separate file from the component.** You will rewrite the wording twenty times.
- **One `isBusy` guard on every clickable element.** Double-clicks are the number-one live failure.
- **Clear every timer** on new turn and on unmount, or a leftover interval will type into the next scene.
- **Never read state inside a timer** — mirror it in a ref. Stale closures cause infinite scene loops.
- **Budget the runtime.** Five beats per turn is roughly 8 to 12 seconds. Eight turns is already two
  minutes of animation plus your commentary. Count it, out loud, with a stopwatch.
- **Label an obviously simulated surface as simulated.** A discreet "Simulated view — for demo
  purposes only" under a fake third-party screen costs nothing and protects your credibility.
- **Keep a fallback.** Screen-record the full run before presenting.
- **Never put real customer data or PII in the script.** It ends up in a public repo eventually.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| The same scene replays forever | Stale `sceneIndex` read inside a `setTimeout` | Read `sceneIndexRef.current` |
| Two messages interleave | Missing `isBusy` guard, or timers not cleared | Guard every button, call `clearAllTimers()` on turn start |
| Long answers take forever | Fixed characters-per-tick | Use `step = max(1, round(length / 110))` |
| Feels like a video, not a product | Single linear path, no interaction | Offer 2-3 choices per scene, add one interactive card |
| Reveal looks glitchy on a table | Animating structured content | Commit cards fully formed, no reveal |
| Typing looks robotic | Chunked user typing | One character per tick for the user message |
