# /motion - Add Animations and Motion

You are enhancing UI components with production-ready animations using Framer Motion.

## Your Task
Add animations and interactive motion to existing or new components with:
- **Framer Motion library integration** (latest version)
- **Performance-optimized animations** (60fps target)
- **Accessibility-friendly motion** (respects prefers-reduced-motion)
- **Smooth transitions and micro-interactions**
- **TypeScript-typed animation variants**

## Animation Types

### Entrance Animations
- **Fade in:** Opacity 0 → 1
- **Slide in:** Translate from edge + fade
- **Scale in:** Scale 0.8 → 1 + fade
- **Stagger:** Sequential entrance for lists

### Exit Animations
- **Fade out:** Opacity 1 → 0
- **Slide out:** Translate to edge + fade
- **Scale out:** Scale 1 → 0.8 + fade

### Interactive Animations
- **Hover:** Scale, shadow, color transitions
- **Tap/Click:** Press effect, ripple
- **Focus:** Outline, scale, highlight
- **Drag:** Drag constraints, momentum

### Scroll Animations
- **Parallax:** Different scroll speeds
- **Reveal on scroll:** Fade/slide in when visible
- **Scroll progress:** Progress bars, indicators

### Loading Animations
- **Skeleton:** Shimmer loading state
- **Spinner:** Rotating loader
- **Progress:** Linear/circular progress bars
- **Pulse:** Breathing effect

## Process
1. **Analyze component** for animation opportunities
2. **Create Framer Motion variants** with TypeScript types
3. **Add motion components** with accessibility
4. **Validate performance** (no jank, 60fps)
5. **Include prefers-reduced-motion alternative**

## Output Format
- **Component code** with Framer Motion integration
- **Animation variants** (TypeScript typed)
- **Performance notes** (GPU acceleration, will-change)
- **Accessibility compliance** check (reduced motion support)
- **Token usage and cost estimate**

## Animation Standards
- Use `motion` components from Framer Motion
- Define variants for reusable animations
- Add `whileHover`, `whileTap`, `whileFocus` where appropriate
- Respect `prefers-reduced-motion` media query
- Use hardware-accelerated properties (transform, opacity)
- Avoid layout shifts during animations
- Add proper exit animations for unmounting

## Example Usage
```
/motion Add slide-in animation to sidebar
/motion Create loading skeleton for card component
/motion Add hover effects to button with scale and shadow
/motion Build stagger animation for list items
/motion Create parallax scroll effect for hero section
/motion Add drag and drop with constraints
```

## Advanced Options
You can request specific features:
- **Duration:** "with 300ms duration"
- **Easing:** "with spring physics" or "with ease-in-out"
- **Delay:** "with 100ms stagger delay"
- **Trigger:** "on scroll into view" or "on hover"
- **Reduced Motion:** "with simplified animation for prefers-reduced-motion"

## Quality Gates
All animations must pass:
1. 60fps performance (no jank)
2. Reduced motion alternative provided
3. GPU acceleration used (transform/opacity)
4. No layout shifts (use transform, not width/height)
5. Proper cleanup on unmount (no memory leaks)

## Performance Tips
- Use `transform` and `opacity` (GPU-accelerated)
- Avoid animating `width`, `height`, `left`, `top`
- Use `will-change` sparingly
- Implement `AnimatePresence` for exit animations
- Use `layoutId` for shared element transitions

---

**Ask the user what animations they want to add.**
