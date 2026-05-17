# X.com Automation Skill

## ⚠️ IMPORTANT: Don't Auto-Close Browser

**SAU KHI HOÀN THÀNH TASK AUTOMATION, KHÔNG ĐÓNG BROWSER!**

---

## 🎯 Core Principles (MUST FOLLOW)

### 1. READ Before Action
- Read the actual content
- Understand context/situation  
- DON'T jump straight into code

### 2. KISS - Keep It Simple
- Simple click() > complex JS
- First solution = simplest solution
- Don't over-engineer

### 3. Quality Over Quantity
- Meaningful, specific comments > generic templates
- Do it right once > do it wrong 10 times

---

## 🔑 Working Selectors (X.com)

```
[data-testid="retweet"]         → repost button
[data-testid="retweetConfirm"]  → confirm repost in menu
[data-testid="tweetTextarea_0"]  → quote compose textarea
[data-testid="tweetButton"]      → post button
[role="menu"]                    → dropdown menu
[role="menuitem"]                → menu items
```

---

## 📋 Quote Repost Workflow

```
1. page.goto(url)
2. WAIT for content to load
3. READ the tweet content (first ~300 chars)
4. THINK about what comment fits
5. WRITE comment relevant to content
6. click([data-testid="retweet"])
7. WAIT for menu
8. Find and click "Quote" in menu
9. WAIT for compose modal
10. fill textarea with your thoughtful comment
11. click([data-testid="tweetButton"])
12. WAIT for success
```

---

## 📋 Simple Repost Workflow

```
1. page.goto(url)
2. READ content
3. click([data-testid="retweet"])
4. WAIT
5. click([data-testid="retweetConfirm"])
```

---

## 🔴 Always Remember

1. **READ content first** - understand what you're interacting with
2. **Write meaningful comments** - not generic templates
3. **Simple code** - don't add complexity if not needed
4. **Test simple first** - complex only if simple fails
5. **Don't close browser** - keep open for user inspection

---

## 🚫 Anti-Patterns

- ❌ Generic comments for all posts
- ❌ Pattern matching instead of reading content
- ❌ Complex JS when simple click() works
- ❌ Over-engineering simple tasks
- ❌ Debugging for 30+ minutes when solution is simple

---

## 📁 Related Files

- `pre-automation-checklist.md` - checklist to follow
- `x-com-automation-lessons.md` - lessons learned
- `references/scripts.py` - working automation scripts

---

Last updated: 2026-05-17