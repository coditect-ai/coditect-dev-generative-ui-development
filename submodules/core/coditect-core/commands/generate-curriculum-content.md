---
name: generate-curriculum-content
description: Generate comprehensive AI curriculum content across multiple skill levels with NotebookLM optimization, assessment integration, and pedagogical frameworks
---

# CURRICULUM CONTENT GENERATION MODE

Generate comprehensive educational content for: $ARGUMENTS

## Mode Rules

### ✅ ALLOWED ACTIVITIES
- **Multi-level content generation** across 4 skill levels
- **Learning objective creation** using Bloom's taxonomy
- **Assessment framework design** with adaptive evaluation
- **NotebookLM metadata optimization** for AI processing
- **Cross-reference creation** for knowledge graph building
- **Pedagogical framework application** (scaffolding, constructivist learning)

### ❌ FORBIDDEN ACTIVITIES  
- **Single-level content only** - Must address multiple skill levels
- **Assessment-free content** - Must integrate evaluation
- **Generic content** - Must be AI-domain specific
- **Metadata-poor content** - Must optimize for NotebookLM

## Content Generation Framework

### Phase 1: Learning Architecture Design
```markdown
## Learning Objectives by Skill Level

### Beginner (Bloom Distribution: Remember 40%, Understand 35%, Apply 20%, Analyze 5%)
- [ ] **Remember**: [Specific recall objective]
- [ ] **Understand**: [Conceptual understanding objective]  
- [ ] **Apply**: [Basic application objective]

### Intermediate (Bloom Distribution: Understand 25%, Apply 35%, Analyze 20%, Evaluate 5%)
- [ ] **Understand**: [Detailed comprehension objective]
- [ ] **Apply**: [Implementation objective]
- [ ] **Analyze**: [Comparison/analysis objective]

### Advanced (Bloom Distribution: Apply 25%, Analyze 30%, Evaluate 20%, Create 5%)
- [ ] **Apply**: [Complex implementation objective]
- [ ] **Analyze**: [Research analysis objective]
- [ ] **Evaluate**: [Critical evaluation objective]

### Expert (Bloom Distribution: Apply 25%, Analyze 25%, Evaluate 20%, Create 15%)
- [ ] **Analyze**: [Theoretical analysis objective]
- [ ] **Evaluate**: [Peer review/critique objective]
- [ ] **Create**: [Innovation/research objective]

## Prerequisites Assessment
- **Beginner**: [List foundational requirements]
- **Intermediate**: [List technical prerequisites] 
- **Advanced**: [List specialized knowledge needed]
- **Expert**: [List research-level requirements]
```

### Phase 2: Multi-Level Content Creation

**Beginner Content Pattern**:
```markdown
# [Topic] for Absolute Beginners

## Learning Story: [Character]'s Journey
[Narrative approach with relatable character learning the concept]

### What is [Topic]? (Simple Definition)
[Everyday language explanation with analogies]

### Visual Analogy: [Real-World Comparison]
[Concrete example from daily life that mirrors the AI concept]

### Simple Example: [Guided Walkthrough]
[Step-by-step example with explanations]

### Key Takeaways
- [3-5 memorable bullet points]

### Check Your Understanding
- [Simple quiz questions focusing on recognition and basic comprehension]

### Next Steps
[Preview of intermediate level with encouragement]
```

**Intermediate Content Pattern**:
```markdown
# [Topic] in Practice

## Project Overview
[Real-world application project]

### Learning Goals
- [Specific implementation objectives]

### Tools and Technologies
- [Required software, libraries, frameworks]

### Step-by-Step Implementation
#### Part 1: [Foundation Setup]
#### Part 2: [Core Implementation]  
#### Part 3: [Testing and Validation]
#### Part 4: [Optimization and Enhancement]

### Expected Outcomes
- [Measurable deliverables]
- [Portfolio additions]

### Troubleshooting Guide
[Common issues and solutions]

### Extension Challenges
[Additional features to implement]
```

**Advanced Content Pattern**:
```markdown
# Advanced [Topic]: Research and Optimization

## Research Context
[Current state of the field and open problems]

### Paper Analysis
[2-3 recent papers with implementation insights]

### Optimization Challenges
[Performance, scalability, accuracy improvements]

### Implementation Deep-Dive
[Complex algorithm implementation with mathematical foundations]

### Evaluation Framework
[Rigorous testing and benchmarking methodologies]

### Case Studies
[Industry applications and real-world deployments]

### Research Opportunities
[Open problems and potential research directions]
```

**Expert Content Pattern**:
```markdown
# [Topic] Research Frontiers

## Theoretical Foundations
[Mathematical frameworks and formal analysis]

### Current Research Landscape
[Survey of latest developments and breakthrough papers]

### Innovation Challenge
[Original research problem to solve]

### Methodology Requirements
[Research design, experimental protocols, evaluation criteria]

### Contribution Pathways
[Publication venues, collaboration opportunities, impact measurement]

### Theoretical Analysis
[Formal proofs, complexity analysis, theoretical guarantees]

### Future Directions
[Long-term research vision and societal impact]
```

### Phase 3: Assessment Integration

```markdown
## Assessment Framework by Skill Level

### Formative Assessment (Embedded Throughout)
**Beginner**: 
- Concept check questions every 2 paragraphs
- Visual identification exercises
- Simple recall quizzes

**Intermediate**:
- Code checkpoint validations  
- Mini-project milestones
- Peer code review exercises

**Advanced**:
- Research paper analysis assignments
- Optimization challenge checkpoints
- Case study evaluations

**Expert**:
- Literature review submissions
- Original research proposal drafts
- Peer critique assignments

### Summative Assessment (End of Module)
**Beginner**:
- Multiple choice quiz (20 questions)
- Concept explanation project
- Learning reflection essay

**Intermediate**:
- Complete implementation project
- Technical presentation
- Portfolio documentation

**Advanced**:
- Research implementation project
- Performance optimization report
- System design document

**Expert**:
- Original research contribution
- Publication-quality paper
- Conference presentation
```

### Phase 4: NotebookLM Optimization

```yaml
# Content Metadata Template
content_metadata:
  # Core Identifiers
  skill_level: [beginner|intermediate|advanced|expert]
  module: "module[X]_[topic]"
  week: [week_number]
  topic: "[specific_topic]"
  
  # Learning Structure  
  estimated_time_hours: [X]
  difficulty_score: [1-5]
  bloom_levels: [list of cognitive levels]
  learning_objectives: [specific objectives]
  prerequisites: [required knowledge]
  
  # Content Organization
  content_type: [concept|example|exercise|project|assessment]
  format: [markdown|jupyter|interactive|video|audio]
  language_complexity: [elementary|intermediate|advanced|graduate]
  
  # Cross-References (Knowledge Graph)
  related_concepts: [connected topics]
  prerequisite_topics: [foundational concepts]  
  follow_up_topics: [next learning steps]
  cross_module_connections: [links to other modules]
  
  # Assessment Integration
  formative_assessments: [embedded evaluations]
  summative_assessments: [module-level tests]
  project_connections: [related hands-on work]
  portfolio_items: [progressive skill documentation]
  
  # Accessibility and Personalization
  learning_styles: [visual|auditory|kinesthetic|reading]
  accommodation_features: [accessibility adaptations]
  personalization_markers: [adaptive content triggers]
  
  # NotebookLM Enhancement
  ai_generation_ready: true
  book_chapter_structure: [hierarchical organization]
  quiz_question_seeds: [assessment generation prompts]
  flashcard_concepts: [key terms and definitions]
  interactive_elements: [engagement opportunities]
```

## Content Generation Strategies

### Strategy 1: Progressive Complexity Scaling
```
1. Identify core concept at expert level
2. Abstract to essential elements
3. Scale down complexity for each level:
   - Expert: Full mathematical rigor + research context
   - Advanced: Algorithmic details + optimization focus  
   - Intermediate: Implementation focus + practical applications
   - Beginner: Conceptual understanding + visual analogies
4. Ensure concept integrity across all levels
5. Create progression bridges between adjacent levels
```

### Strategy 2: Assessment-Driven Content Design
```
1. Design assessments first for each skill level
2. Work backward to determine required content
3. Ensure alignment between content and evaluation
4. Integrate formative assessment throughout
5. Create clear performance criteria and rubrics
```

### Strategy 3: Knowledge Graph Integration
```
1. Map concept relationships and dependencies
2. Create explicit cross-references between topics
3. Design prerequisite validation checkpoints
4. Build knowledge progression pathways
5. Enable adaptive content navigation
```

## Output Structure Template

```markdown
# Generated Content: [Topic] - [Skill Level] Level

## Content Metadata
[YAML metadata block]

## Learning Objectives
- [Bloom Level]: [Specific objective with assessment method]

## Prerequisites Verification
- [ ] [Prerequisite 1] (validation method)
- [ ] [Prerequisite 2] (validation method)

## Content Structure
### Core Concepts ([Appropriate Complexity Level])
[Level-appropriate content delivery]

### Hands-On Activities ([Skill-Appropriate Format])
[Practical exercises matching skill level]

### Assessment Integration ([Embedded Evaluation])
[Formative assessment throughout]

### Real-World Applications ([Level-Relevant Examples])
[Industry connections and use cases]

## Cross-References
- **Prerequisite Topics**: [foundational concepts with links]
- **Related Concepts**: [parallel topics with connections]
- **Next Learning Steps**: [progression pathway]

## Assessment Components
### Formative Assessment
[Embedded evaluation throughout content]

### Summative Assessment  
[End-of-section comprehensive evaluation]

### Portfolio Integration
[Progressive skill documentation opportunities]

## NotebookLM Optimization
- **Book Generation Ready**: [structured for chapter creation]
- **Quiz Seeds**: [assessment generation prompts]
- **Flashcard Concepts**: [key terms for memorization]
- **Interactive Elements**: [engagement opportunities]

## Quality Assurance Checklist
- [ ] **Learning Objective Alignment**: Content matches stated objectives
- [ ] **Skill Level Appropriateness**: Cognitive load matches target level
- [ ] **Assessment Integration**: Evaluation aligns with content and objectives
- [ ] **Cross-Reference Accuracy**: Links and dependencies verified
- [ ] **Technical Accuracy**: Code examples tested and validated
- [ ] **Accessibility Features**: Multiple learning styles accommodated
- [ ] **NotebookLM Optimization**: Metadata and structure optimized
```

## Integration Requirements

### Skills Integration
- Auto-load: `ai-curriculum-development` skill for comprehensive framework
- Coordinate: `assessment-creation` skill for evaluation design
- Reference: `notebooklm-optimization` skill for content formatting

### Agent Coordination  
- Use: `ai-curriculum-specialist` for overall curriculum architecture
- Delegate: Content generation to specialized educational agents
- Validate: Quality and pedagogy with educational review agents

### Command Workflows
- Precede: `/research` mode to validate educational approaches
- Follow: `/optimize-notebooklm` for content enhancement  
- Integrate: `/generate-assessment` for evaluation creation

## Best Practices

✅ **DO**:
- Start with clear learning objectives for each skill level
- Apply Bloom's taxonomy distribution appropriate to skill level
- Integrate assessment throughout the learning experience
- Create explicit cross-references and knowledge connections
- Test content with target skill level learners
- Optimize metadata for NotebookLM processing
- Ensure accessibility across diverse learning needs

❌ **DON'T**:
- Create content for only one skill level
- Skip learning objective definition
- Ignore assessment integration
- Create isolated content without connections
- Use inappropriate cognitive complexity for skill level
- Neglect NotebookLM optimization metadata
- Forget accessibility and inclusion considerations

## Quality Validation

### Content Quality Metrics
- Learning objective achievement: 90%+ of learners meet objectives
- Skill progression rate: 80%+ advance to next level successfully  
- Engagement metrics: 85%+ completion rate across skill levels
- Technical accuracy: 100% code functionality and concept validity

### Assessment Quality Metrics  
- Content-assessment alignment: Strong correlation between teaching and testing
- Skill differentiation: Clear performance differences across skill levels
- Bias detection: <5% performance gaps across demographic groups
- Accessibility compliance: Full WCAG 2.1 AA standard adherence