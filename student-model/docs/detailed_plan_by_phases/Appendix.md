## Appendix: Example Session Flow

### Complete Integrated Workflow

**Session 7: Understanding React Context API in Monkeytype**

```bash
# PHASE 1: Conceptual Context
terminal1:~/student-model$ python student.py show "React Context API"
terminal1:~/student-model$ python student.py related "React Context API"
```

_[Paste into Claude]_

```
📊 Concept: React Context API
   Mastery:     45%
   Confidence:  low
   ⚠️  Struggles:
      - how provider connects to consumers

🔗 Concepts related to 'React Context API':
   - React Hooks (Mastery: 60%, Last: 2 days ago) ✓
   - JavaScript Closures (Mastery: 55%, Last: 1 week ago) ⚠️ LOW
```

---

**Claude:** _"I see you're at 45% mastery with Context API and struggling with the provider-consumer pattern. Before we start, what are you currently investigating?"_

**You:** _"I'm looking at monkeytype's theme system. Components use 'theme' but I can't find where it's passed as a prop."_

---

```bash
# PHASE 2: Concrete Context
terminal2:~/monkeytype$ cat packages/frontend/src/components/TestArea.tsx | grep -B 5 -A 5 "theme"
```

_[Paste output into Claude]_

---

**Claude:** _"Perfect. This is exactly where your struggle lives. I see `useContext(ThemeContext)` on line 50. What do you think useContext() does?"_

**You:** _"Gets the theme somehow?"_

**Claude:** _"Right direction. Let's find where ThemeContext is created. Can you run: `grep -r 'ThemeContext' --include='_.tsx' packages/frontend/src/`"\*

---

```bash
terminal2:~/monkeytype$ grep -r 'ThemeContext' --include='*.tsx' packages/frontend/src/
```

_[Paste output]_

---

**Claude:** _"Excellent evidence! Look at App.tsx - do you see the pattern?"_

**You:** _"There's a ThemeProvider wrapping stuff..."_

**Claude:** _"Exactly! This is the provider-consumer pattern you marked as a struggle. Let's see the Provider: `cat packages/frontend/src/contexts/ThemeContext.tsx`"_

---

```bash
terminal2:~/monkeytype$ cat packages/frontend/src/contexts/ThemeContext.tsx
```

_[Paste output]_

---

**Claude:** _"Now let's connect all three pieces: [synthesis]. Does this trace clarify that connection?"_

**You:** _"Oh! The Provider puts the value in the tunnel, and useContext pulls it out?"_

**Claude:** _"Perfect! Let's update your model to capture this breakthrough."_

---

```bash
# PHASE 3: Session End
terminal1:~/student-model$ python student.py session-end \
  --update "React Context API:60:medium" \
  --breakthrough "React Context API:understood provider-consumer as tunnel metaphor by tracing ThemeContext" \
  --struggle "React Context API:when to use Context vs props - performance implications?"

terminal1:~/student-model$ code SESSION_07_context_api.md
```

---

This example shows how the two systems work together seamlessly:

- **Student Model** provided high-level conceptual context (45% mastery, known struggle)
- **Workspace Protocol** provided concrete evidence (actual code, grep results)
- **Claude** bridged both to create targeted, grounded learning experience