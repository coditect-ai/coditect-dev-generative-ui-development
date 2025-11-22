# Pre-Built Evaluation Rubrics

Collection of ready-to-use evaluation rubrics for different domains.

## Code Quality Rubric

### Correctness (30%)
| Score | Description |
|-------|-------------|
| 5 | Handles all cases including edge cases, no bugs |
| 4 | Handles main cases correctly, minor edge case issues |
| 3 | Core functionality works, some edge case bugs |
| 2 | Core functionality has bugs |
| 1 | Does not work as intended |

### Code Structure (20%)
| Score | Description |
|-------|-------------|
| 5 | Well-organized, clear separation of concerns, DRY |
| 4 | Organized, minor repetition |
| 3 | Functional organization, some repetition |
| 2 | Poor organization, significant repetition |
| 1 | Unstructured, unmaintainable |

### Error Handling (15%)
| Score | Description |
|-------|-------------|
| 5 | Comprehensive error handling with recovery, detailed messages |
| 4 | Good error handling, clear messages |
| 3 | Basic error handling present |
| 2 | Minimal error handling |
| 1 | No error handling |

### Documentation (10%)
| Score | Description |
|-------|-------------|
| 5 | Comprehensive docs, examples, edge cases documented |
| 4 | Good documentation coverage |
| 3 | Basic documentation present |
| 2 | Minimal documentation |
| 1 | No documentation |

### Type Safety (10%)
| Score | Description |
|-------|-------------|
| 5 | Full type hints, passes strict type checking |
| 4 | Good type coverage (>80%) |
| 3 | Basic type hints (>50%) |
| 2 | Minimal type hints (<50%) |
| 1 | No type hints |

### Performance (10%)
| Score | Description |
|-------|-------------|
| 5 | Optimal algorithms, efficient implementation |
| 4 | Good performance, room for minor optimization |
| 3 | Acceptable performance |
| 2 | Performance issues |
| 1 | Unacceptable performance |

### Security (5%)
| Score | Description |
|-------|-------------|
| 5 | Security best practices, input validation, no vulnerabilities |
| 4 | Good security practices |
| 3 | Basic security measures |
| 2 | Security concerns present |
| 1 | Critical security issues |

---

## Architecture Quality Rubric

### Scalability (25%)
| Score | Description |
|-------|-------------|
| 5 | Scales horizontally, handles 10x growth |
| 4 | Scales with minor modifications |
| 3 | Handles current load |
| 2 | Scaling issues likely |
| 1 | Cannot scale |

### Maintainability (20%)
| Score | Description |
|-------|-------------|
| 5 | Clear boundaries, easy to modify, well-tested |
| 4 | Generally maintainable |
| 3 | Can be maintained with effort |
| 2 | Difficult to maintain |
| 1 | Unmaintainable |

### Observability (15%)
| Score | Description |
|-------|-------------|
| 5 | Comprehensive metrics, logging, tracing |
| 4 | Good observability coverage |
| 3 | Basic logging/metrics |
| 2 | Minimal observability |
| 1 | No observability |

### Fault Tolerance (15%)
| Score | Description |
|-------|-------------|
| 5 | Circuit breakers, retries, graceful degradation |
| 4 | Good error recovery |
| 3 | Basic error handling |
| 2 | Poor fault tolerance |
| 1 | No fault tolerance |

### Security (15%)
| Score | Description |
|-------|-------------|
| 5 | Defense in depth, least privilege, validated inputs |
| 4 | Good security practices |
| 3 | Basic security |
| 2 | Security gaps |
| 1 | Critical vulnerabilities |

### Documentation (10%)
| Score | Description |
|-------|-------------|
| 5 | Architecture diagrams, ADRs, runbooks |
| 4 | Good documentation |
| 3 | Basic documentation |
| 2 | Minimal documentation |
| 1 | No documentation |

---

## Multi-Agent System Rubric

### Coordination Efficiency (25%)
| Score | Description |
|-------|-------------|
| 5 | Minimal coordination overhead, async patterns |
| 4 | Efficient coordination |
| 3 | Acceptable coordination |
| 2 | High coordination overhead |
| 1 | Coordination bottleneck |

### Error Cascade Prevention (20%)
| Score | Description |
|-------|-------------|
| 5 | Circuit breakers, bulkheads, timeouts everywhere |
| 4 | Good isolation |
| 3 | Basic isolation |
| 2 | Error cascade risk |
| 1 | No isolation |

### Token Economics (15%)
| Score | Description |
|-------|-------------|
| 5 | Optimized token usage, checkpointing, compression |
| 4 | Good token management |
| 3 | Acceptable token usage |
| 2 | High token consumption |
| 1 | Excessive token waste |

### Observability (15%)
| Score | Description |
|-------|-------------|
| 5 | Full tracing, agent state visibility, debug tools |
| 4 | Good observability |
| 3 | Basic logging |
| 2 | Limited visibility |
| 1 | No observability |

### Delegation Clarity (15%)
| Score | Description |
|-------|-------------|
| 5 | Clear responsibilities, typed interfaces, boundaries |
| 4 | Clear delegation |
| 3 | Understandable delegation |
| 2 | Unclear responsibilities |
| 1 | Chaotic delegation |

### Checkpoint/Resume (10%)
| Score | Description |
|-------|-------------|
| 5 | Comprehensive checkpointing, resume from any state |
| 4 | Good checkpoint coverage |
| 3 | Basic checkpointing |
| 2 | Limited checkpointing |
| 1 | No checkpointing |

---

## API Design Rubric

### RESTful Design (30%)
| Score | Description |
|-------|-------------|
| 5 | Fully RESTful, consistent resource modeling, HATEOAS |
| 4 | Good REST practices, minor inconsistencies |
| 3 | Mostly RESTful with some non-standard endpoints |
| 2 | Poor REST design, mixing paradigms |
| 1 | Not RESTful, RPC-style |

### Response Times (20%)
| Score | Description |
|-------|-------------|
| 5 | < 100ms p99 for all endpoints |
| 4 | < 200ms p99 for most endpoints |
| 3 | < 500ms p99 acceptable |
| 2 | > 500ms p99 for many endpoints |
| 1 | > 1000ms p99 unacceptable |

### Error Handling (20%)
| Score | Description |
|-------|-------------|
| 5 | Clear error codes, actionable messages, RFC 7807 compliance |
| 4 | Good error messages with codes |
| 3 | Basic error messages |
| 2 | Generic error messages |
| 1 | No error messages or stack traces exposed |

### Versioning (10%)
| Score | Description |
|-------|-------------|
| 5 | Semantic versioning, backward compatibility, deprecation policy |
| 4 | Good versioning strategy |
| 3 | Basic versioning |
| 2 | Inconsistent versioning |
| 1 | No versioning |

### Documentation (10%)
| Score | Description |
|-------|-------------|
| 5 | OpenAPI spec, examples, interactive docs, changelog |
| 4 | Good API documentation |
| 3 | Basic documentation |
| 2 | Minimal documentation |
| 1 | No documentation |

### Security (10%)
| Score | Description |
|-------|-------------|
| 5 | OAuth2/OIDC, rate limiting, input validation, HTTPS only |
| 4 | Good security practices |
| 3 | Basic security (auth + HTTPS) |
| 2 | Security gaps |
| 1 | Critical vulnerabilities |

---

## Database Design Rubric

### Schema Design (30%)
| Score | Description |
|-------|-------------|
| 5 | Normalized, efficient indexes, proper constraints |
| 4 | Good schema design, minor optimization opportunities |
| 3 | Functional schema with some inefficiencies |
| 2 | Poor normalization or missing constraints |
| 1 | Broken schema design |

### Query Performance (25%)
| Score | Description |
|-------|-------------|
| 5 | All queries optimized, proper indexes, < 10ms |
| 4 | Good query performance, < 50ms |
| 3 | Acceptable performance, < 200ms |
| 2 | Slow queries, > 200ms |
| 1 | Unacceptable performance, > 1s |

### Data Integrity (20%)
| Score | Description |
|-------|-------------|
| 5 | Foreign keys, constraints, transactions, ACID compliance |
| 4 | Good data integrity |
| 3 | Basic integrity constraints |
| 2 | Missing constraints |
| 1 | No data integrity |

### Scalability (15%)
| Score | Description |
|-------|-------------|
| 5 | Sharding ready, read replicas, caching layer |
| 4 | Can scale with modifications |
| 3 | Handles current load |
| 2 | Scaling issues likely |
| 1 | Cannot scale |

### Migration Strategy (10%)
| Score | Description |
|-------|-------------|
| 5 | Zero-downtime migrations, rollback capability, versioned |
| 4 | Good migration strategy |
| 3 | Basic migrations |
| 2 | Risky migrations |
| 1 | No migration strategy |

---

## Testing Quality Rubric

### Coverage (30%)
| Score | Description |
|-------|-------------|
| 5 | > 90% coverage, all critical paths tested |
| 4 | 80-90% coverage |
| 3 | 60-80% coverage |
| 2 | < 60% coverage |
| 1 | < 30% coverage or no tests |

### Test Quality (25%)
| Score | Description |
|-------|-------------|
| 5 | Meaningful tests, edge cases, integration tests |
| 4 | Good test quality |
| 3 | Basic tests present |
| 2 | Poor test quality (trivial tests) |
| 1 | No meaningful tests |

### Test Organization (15%)
| Score | Description |
|-------|-------------|
| 5 | Well-organized, clear naming, fixtures, mocks |
| 4 | Good organization |
| 3 | Basic organization |
| 2 | Poor organization |
| 1 | Chaotic test structure |

### CI/CD Integration (15%)
| Score | Description |
|-------|-------------|
| 5 | Automated tests in CI, coverage reports, fail on < threshold |
| 4 | Good CI integration |
| 3 | Basic CI testing |
| 2 | Manual testing |
| 1 | No CI integration |

### Performance Tests (10%)
| Score | Description |
|-------|-------------|
| 5 | Load tests, stress tests, benchmarks in CI |
| 4 | Good performance testing |
| 3 | Basic performance tests |
| 2 | Minimal performance testing |
| 1 | No performance tests |

### Mutation Testing (5%)
| Score | Description |
|-------|-------------|
| 5 | Mutation testing integrated, high mutation score |
| 4 | Mutation testing present |
| 3 | Experimenting with mutation testing |
| 2 | Aware of concept |
| 1 | No mutation testing |
