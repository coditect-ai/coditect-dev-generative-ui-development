# TOON Module - Technical Specification

**Version:** 1.0.0
**Status:** Draft - Ready for Review
**Date:** 2025-11-17
**Author:** CODITECT Platform Team

---

## Executive Summary

The TOON Module is a **pluggable, configurable token optimization system** for the CODITECT framework, providing 35-45% token reduction through TOON format encoding/decoding with zero disruption to existing systems.

### Key Design Principles

1. **Modular** - Drop-in module with clean interfaces
2. **Configurable** - Toggle on/off via environment variables or config files
3. **Multi-Purpose** - Works for storage, LLM I/O, checkpoints, exports
4. **Backward Compatible** - Existing systems work unchanged when TOON is disabled
5. **Format Agnostic** - Supports dual-format (TOON + Markdown/JSON)
6. **Performance First** - Minimal overhead, lazy loading, caching

---

## Architecture Overview

### Module Structure

```
scripts/core/toon_module/
├── __init__.py                 # Public API exports
├── config.py                   # Configuration management
├── encoders/
│   ├── __init__.py
│   ├── base.py                # Base encoder interface
│   ├── toon_encoder.py        # TOON format encoder
│   ├── json_encoder.py        # JSON encoder (fallback)
│   └── markdown_encoder.py    # Markdown encoder
├── decoders/
│   ├── __init__.py
│   ├── base.py                # Base decoder interface
│   ├── toon_decoder.py        # TOON format decoder
│   ├── json_decoder.py        # JSON decoder
│   └── markdown_decoder.py    # Markdown decoder
├── adapters/
│   ├── __init__.py
│   ├── storage_adapter.py     # File system storage
│   ├── llm_adapter.py         # LLM I/O optimization
│   ├── checkpoint_adapter.py  # Checkpoint integration
│   └── export_adapter.py      # Export processing
├── converters/
│   ├── __init__.py
│   ├── toon_to_markdown.py   # TOON → Markdown
│   ├── toon_to_json.py       # TOON → JSON
│   ├── markdown_to_toon.py   # Markdown → TOON
│   └── json_to_toon.py       # JSON → TOON
├── utils/
│   ├── __init__.py
│   ├── validators.py          # Schema validation
│   ├── metrics.py             # Token counting, savings tracking
│   └── cache.py               # In-memory caching
└── tests/
    ├── test_encoders.py
    ├── test_decoders.py
    ├── test_adapters.py
    └── test_converters.py
```

---

## Configuration System

### 1. Environment Variables

```bash
# Enable/disable TOON globally
export TOON_ENABLED=true              # Default: false

# Storage format (toon, json, markdown, dual)
export TOON_STORAGE_FORMAT=dual       # Default: json

# LLM I/O optimization
export TOON_LLM_INPUT=true            # Encode prompts to TOON
export TOON_LLM_OUTPUT=false          # Keep responses as-is

# Performance tuning
export TOON_CACHE_ENABLED=true        # In-memory cache
export TOON_CACHE_SIZE_MB=50          # Cache size limit

# Monitoring
export TOON_METRICS_ENABLED=true      # Track token savings
export TOON_METRICS_FILE=metrics.json # Savings report
```

### 2. Configuration File

**`.toonrc` or `toon.config.json`:**

```json
{
  "enabled": true,
  "storage": {
    "format": "dual",
    "primary": "toon",
    "fallback": "json",
    "auto_convert": true,
    "preserve_original": true
  },
  "llm": {
    "input_encoding": true,
    "output_encoding": false,
    "max_size_kb": 100,
    "cache_prompts": true
  },
  "adapters": {
    "storage": {
      "enabled": true,
      "path": "MEMORY-CONTEXT/dedup_state"
    },
    "checkpoint": {
      "enabled": true,
      "path": "CHECKPOINTS"
    },
    "export": {
      "enabled": true,
      "path": "MEMORY-CONTEXT/exports"
    }
  },
  "performance": {
    "lazy_loading": true,
    "batch_size": 100,
    "parallel_processing": true
  },
  "monitoring": {
    "track_savings": true,
    "report_interval_hours": 24,
    "alert_threshold_mb": 10
  }
}
```

### 3. Python API Configuration

```python
from toon_module import TOONConfig

# Option 1: Use defaults + environment variables
config = TOONConfig.from_env()

# Option 2: Load from config file
config = TOONConfig.from_file('.toonrc')

# Option 3: Programmatic configuration
config = TOONConfig(
    enabled=True,
    storage_format='dual',
    llm_input_encoding=True,
    cache_enabled=True
)

# Option 4: Runtime override
config.enable()
config.disable()
config.set_format('toon')
```

---

## Core API Design

### 1. Simple Public API

```python
# Import everything from one place
from toon_module import (
    # Main encoder/decoder
    encode,
    decode,

    # Format-specific
    encode_toon,
    decode_toon,

    # Adapters
    StorageAdapter,
    LLMAdapter,
    CheckpointAdapter,

    # Converters
    toon_to_markdown,
    markdown_to_toon,

    # Configuration
    TOONConfig,
    is_enabled,

    # Metrics
    get_token_savings,
    get_metrics_report
)
```

### 2. Encoder Interface

```python
from typing import Any, Dict, List, Union
from abc import ABC, abstractmethod

class BaseEncoder(ABC):
    """Base encoder interface for all formats"""

    @abstractmethod
    def encode(self, data: Union[Dict, List]) -> str:
        """Encode data to string format"""
        pass

    @abstractmethod
    def estimate_tokens(self, data: Union[Dict, List]) -> int:
        """Estimate token count before encoding"""
        pass

    @abstractmethod
    def supports(self, data: Any) -> bool:
        """Check if encoder supports this data type"""
        pass


class TOONEncoder(BaseEncoder):
    """TOON format encoder"""

    def encode(self, data: Union[Dict, List]) -> str:
        """
        Encode data to TOON format.

        Examples:
            # Dict → TOON object
            encode({"name": "test", "value": 123})
            # → "name: test\nvalue: 123"

            # List[Dict] → TOON tabular array
            encode([{"id": 1, "name": "A"}, {"id": 2, "name": "B"}])
            # → "items[2]{id,name}:\n 1,A\n 2,B"
        """
        if isinstance(data, list) and data and isinstance(data[0], dict):
            return self._encode_tabular_array(data)
        elif isinstance(data, dict):
            return self._encode_object(data)
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    def estimate_tokens(self, data: Union[Dict, List]) -> int:
        """Estimate tokens using tiktoken"""
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        preview = self.encode(data)
        return len(enc.encode(preview))

    def supports(self, data: Any) -> bool:
        """TOON supports dicts and lists of dicts"""
        return isinstance(data, (dict, list))
```

### 3. Decoder Interface

```python
class BaseDecoder(ABC):
    """Base decoder interface"""

    @abstractmethod
    def decode(self, content: str) -> Union[Dict, List]:
        """Decode string to Python data structure"""
        pass

    @abstractmethod
    def validate(self, content: str) -> bool:
        """Validate format before decoding"""
        pass


class TOONDecoder(BaseDecoder):
    """TOON format decoder"""

    def decode(self, content: str) -> Union[Dict, List]:
        """
        Decode TOON format to Python data.

        Auto-detects:
        - TOON objects → Dict
        - TOON tabular arrays → List[Dict]
        - TOON primitive arrays → List
        """
        if self._is_tabular_array(content):
            return self._decode_tabular_array(content)
        elif self._is_object(content):
            return self._decode_object(content)
        else:
            raise ValueError("Invalid TOON format")

    def validate(self, content: str) -> bool:
        """Validate TOON syntax"""
        try:
            self.decode(content)
            return True
        except Exception:
            return False
```

---

## Adapter Patterns

### 1. Storage Adapter

**Purpose:** Transparent TOON encoding for file storage

```python
from pathlib import Path
from typing import Optional, Union, Dict, List

class StorageAdapter:
    """
    Storage adapter with automatic TOON encoding/decoding.

    Usage:
        storage = StorageAdapter(format='dual')

        # Write (auto-encodes to TOON)
        storage.write('data.toon', my_data)

        # Read (auto-decodes from TOON)
        data = storage.read('data.toon')

        # Dual-format (writes both TOON + JSON)
        storage.write_dual('data', my_data)  # → data.toon + data.json
    """

    def __init__(
        self,
        format: str = 'dual',  # toon, json, markdown, dual
        base_path: Optional[Path] = None,
        encoder: Optional[BaseEncoder] = None,
        decoder: Optional[BaseDecoder] = None
    ):
        self.format = format
        self.base_path = base_path or Path.cwd()
        self.encoder = encoder or self._get_default_encoder()
        self.decoder = decoder or self._get_default_decoder()
        self.config = TOONConfig.from_env()

    def write(
        self,
        filename: str,
        data: Union[Dict, List],
        format_override: Optional[str] = None
    ) -> Path:
        """
        Write data to file with automatic encoding.

        Args:
            filename: Output filename
            data: Data to write
            format_override: Override default format

        Returns:
            Path to written file
        """
        format_to_use = format_override or self.format

        # Skip TOON if disabled
        if not self.config.enabled and format_to_use == 'toon':
            format_to_use = 'json'

        filepath = self.base_path / filename

        if format_to_use == 'dual':
            # Write both TOON and fallback format
            self._write_toon(filepath.with_suffix('.toon'), data)
            self._write_json(filepath.with_suffix('.json'), data)
            return filepath.with_suffix('.toon')

        elif format_to_use == 'toon':
            return self._write_toon(filepath, data)

        elif format_to_use == 'json':
            return self._write_json(filepath, data)

        else:
            raise ValueError(f"Unsupported format: {format_to_use}")

    def read(
        self,
        filename: str,
        format_hint: Optional[str] = None
    ) -> Union[Dict, List]:
        """
        Read and decode file.

        Auto-detects format from extension if not specified.
        Falls back to JSON if TOON read fails.
        """
        filepath = self.base_path / filename

        # Auto-detect format
        if format_hint is None:
            format_hint = filepath.suffix[1:]  # Remove leading dot

        try:
            if format_hint == 'toon':
                return self._read_toon(filepath)
            elif format_hint == 'json':
                return self._read_json(filepath)
            else:
                # Try TOON first, fallback to JSON
                try:
                    return self._read_toon(filepath)
                except:
                    return self._read_json(filepath)
        except FileNotFoundError:
            # Try alternate format if dual-format storage
            if self.format == 'dual':
                alternate = filepath.with_suffix('.json' if format_hint == 'toon' else '.toon')
                return self.read(alternate.name, alternate.suffix[1:])
            raise
```

### 2. LLM Adapter

**Purpose:** Optimize tokens for LLM input/output

```python
class LLMAdapter:
    """
    LLM I/O adapter for automatic prompt optimization.

    Usage:
        llm = LLMAdapter(input_encoding=True)

        # Encode data for prompt (40% token reduction)
        optimized_prompt = llm.encode_for_prompt(checkpoint_data)

        # Send to LLM
        response = claude.messages.create(
            messages=[{"role": "user", "content": optimized_prompt}]
        )

        # Track savings
        savings = llm.get_savings_report()
    """

    def __init__(
        self,
        input_encoding: bool = True,
        output_encoding: bool = False,
        max_size_kb: int = 100,
        cache_enabled: bool = True
    ):
        self.input_encoding = input_encoding
        self.output_encoding = output_encoding
        self.max_size_kb = max_size_kb
        self.cache_enabled = cache_enabled
        self.encoder = TOONEncoder()
        self.decoder = TOONDecoder()
        self.metrics = MetricsTracker()
        self.cache = TTLCache(maxsize=100, ttl=3600) if cache_enabled else None

    def encode_for_prompt(
        self,
        data: Union[Dict, List, str],
        format: str = 'auto'
    ) -> str:
        """
        Encode data for LLM prompt with optimal token usage.

        Args:
            data: Data to encode
            format: Output format (toon, json, markdown, auto)

        Returns:
            Optimized string for LLM consumption
        """
        # Skip encoding if disabled
        if not self.input_encoding:
            return json.dumps(data) if not isinstance(data, str) else data

        # Check cache
        cache_key = self._get_cache_key(data)
        if self.cache and cache_key in self.cache:
            return self.cache[cache_key]

        # Auto-select best format based on data structure
        if format == 'auto':
            format = self._select_optimal_format(data)

        # Encode
        if format == 'toon' and isinstance(data, (dict, list)):
            encoded = self.encoder.encode(data)
        else:
            encoded = json.dumps(data, indent=2)

        # Track metrics
        original_tokens = self._count_tokens(json.dumps(data))
        optimized_tokens = self._count_tokens(encoded)
        self.metrics.record_encoding(original_tokens, optimized_tokens)

        # Cache result
        if self.cache:
            self.cache[cache_key] = encoded

        return encoded

    def create_optimized_message(
        self,
        role: str,
        content: Union[str, Dict, List]
    ) -> Dict[str, str]:
        """
        Create optimized message for Claude API.

        Example:
            msg = llm.create_optimized_message("user", checkpoint_data)
            # → {"role": "user", "content": "checkpoint[1]{...}: ..."}
        """
        optimized_content = self.encode_for_prompt(content)
        return {
            "role": role,
            "content": optimized_content
        }

    def _select_optimal_format(self, data: Any) -> str:
        """
        Select optimal format based on data characteristics.

        Heuristics:
        - List of dicts with consistent schema → TOON tabular (best)
        - Dict with nested structure → TOON object
        - Plain text → unchanged
        - Mixed/complex → JSON
        """
        if isinstance(data, list) and len(data) > 2 and isinstance(data[0], dict):
            # Check if schema is consistent
            if self._has_consistent_schema(data):
                return 'toon'  # Tabular array = best compression

        if isinstance(data, dict):
            return 'toon'  # TOON object

        return 'json'  # Fallback
```

### 3. Checkpoint Adapter

**Purpose:** Integrate TOON into checkpoint creation workflow

```python
class CheckpointAdapter:
    """
    Checkpoint adapter for TOON integration.

    Usage:
        checkpoint = CheckpointAdapter(path='CHECKPOINTS')

        # Create checkpoint with TOON encoding
        checkpoint.create(
            description="Week 1 Day 2 Complete",
            data=checkpoint_data,
            format='dual'  # Creates both .toon and .md
        )

        # Load checkpoint (auto-detects format)
        data = checkpoint.load('2025-11-17-week1-day2')
    """

    def __init__(
        self,
        path: Union[str, Path] = 'CHECKPOINTS',
        auto_convert_markdown: bool = True
    ):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self.auto_convert = auto_convert_markdown
        self.storage = StorageAdapter(base_path=self.path)
        self.converter = TOONToMarkdownConverter()

    def create(
        self,
        description: str,
        data: Dict,
        format: str = 'dual',
        auto_commit: bool = False
    ) -> Path:
        """
        Create checkpoint with TOON encoding.

        Steps:
        1. Generate timestamp and slug
        2. Encode to TOON format
        3. Auto-convert to Markdown (if dual format)
        4. Write both files
        5. Update README
        6. Optionally commit to git
        """
        from datetime import datetime
        import re

        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%SZ')
        slug = re.sub(r'[^a-z0-9]+', '-', description.lower()).strip('-')
        basename = f'{timestamp}-{slug}'

        # Write TOON format
        toon_file = self.storage.write(f'{basename}.toon', data)

        # Auto-convert to Markdown if dual format
        if format == 'dual' and self.auto_convert:
            md_content = self.converter.convert(data)
            md_file = self.path / f'{basename}.md'
            md_file.write_text(md_content)

        # Update README
        self._update_readme(basename, description)

        # Auto-commit if requested
        if auto_commit:
            self._git_commit(basename, description)

        return toon_file

    def load(self, checkpoint_name: str) -> Dict:
        """
        Load checkpoint (auto-detects .toon or .md).

        Prefers TOON for faster parsing and fewer tokens.
        Falls back to Markdown if TOON not available.
        """
        # Try TOON first
        try:
            return self.storage.read(f'{checkpoint_name}.toon')
        except FileNotFoundError:
            pass

        # Fallback to Markdown
        try:
            md_file = self.path / f'{checkpoint_name}.md'
            return self._parse_markdown(md_file.read_text())
        except FileNotFoundError:
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_name}")
```

---

## Converter System

### TOON ↔ Markdown Converter

```python
class TOONToMarkdownConverter:
    """
    Convert TOON format to human-readable Markdown.

    Usage:
        converter = TOONToMarkdownConverter()
        markdown = converter.convert(toon_data)
    """

    def convert(self, data: Union[Dict, str]) -> str:
        """
        Convert TOON data to Markdown.

        Transformations:
        - TOON tabular arrays → Markdown tables
        - TOON objects → YAML-style frontmatter + sections
        - TOON primitive arrays → Bullet lists
        """
        if isinstance(data, str):
            # Parse TOON string first
            decoder = TOONDecoder()
            data = decoder.decode(data)

        if isinstance(data, list):
            return self._array_to_markdown_table(data)
        elif isinstance(data, dict):
            return self._object_to_markdown(data)
        else:
            return str(data)

    def _array_to_markdown_table(self, items: List[Dict]) -> str:
        """
        Convert TOON tabular array to Markdown table.

        TOON:
            tasks[3]{status,priority,title}:
             completed,P0,Create CLI tool
             completed,P0,Fix calculation bug
             pending,P1,Add documentation

        Markdown:
            | Status    | Priority | Title                |
            |-----------|----------|----------------------|
            | completed | P0       | Create CLI tool      |
            | completed | P0       | Fix calculation bug  |
            | pending   | P1       | Add documentation    |
        """
        if not items:
            return ""

        # Get all keys
        keys = list(items[0].keys())

        # Header row
        header = "| " + " | ".join(k.title() for k in keys) + " |"
        separator = "|" + "|".join("-" * (len(k) + 2) for k in keys) + "|"

        # Data rows
        rows = []
        for item in items:
            values = [str(item.get(k, "")) for k in keys]
            rows.append("| " + " | ".join(values) + " |")

        return "\n".join([header, separator] + rows)

    def _object_to_markdown(self, obj: Dict) -> str:
        """
        Convert TOON object to Markdown sections.

        TOON:
            checkpoint:
              timestamp: 2025-11-17T10:30:00Z
              sprint: Week 1 Day 2

        Markdown:
            ## Checkpoint

            **Timestamp:** 2025-11-17T10:30:00Z
            **Sprint:** Week 1 Day 2
        """
        sections = []

        for key, value in obj.items():
            section_title = key.replace('_', ' ').title()
            sections.append(f"## {section_title}\n")

            if isinstance(value, dict):
                for k, v in value.items():
                    label = k.replace('_', ' ').title()
                    sections.append(f"**{label}:** {v}  ")
            elif isinstance(value, list):
                sections.append(self._array_to_markdown_table(value))
            else:
                sections.append(str(value))

            sections.append("\n")

        return "\n".join(sections)


class MarkdownToTOONConverter:
    """Convert Markdown tables back to TOON format"""

    def convert(self, markdown: str) -> str:
        """Parse Markdown and convert to TOON"""
        # Implementation: Parse markdown tables, extract data, encode to TOON
        pass
```

---

## Usage Examples

### Example 1: Deduplication with TOON Storage

```python
from toon_module import StorageAdapter, TOONConfig
from core.conversation_deduplicator import ClaudeConversationDeduplicator

# Enable TOON globally
config = TOONConfig(enabled=True, storage_format='dual')

# Initialize deduplicator with TOON storage
dedup = ClaudeConversationDeduplicator(
    storage_dir='MEMORY-CONTEXT/dedup_state',
    storage_adapter=StorageAdapter(format='dual')  # TOON + JSON
)

# Process export (automatically stores in TOON format)
new_messages, stats = dedup.process_export('session-id', export_data)

# Result: Files created
# - conversation_log.toon (430KB - 50% smaller!)
# - conversation_log.json (861KB - backward compat)
# - content_hashes.json (95KB)
# - watermarks.json (160B)
```

### Example 2: Checkpoint Creation with TOON

```python
from toon_module import CheckpointAdapter

checkpoint = CheckpointAdapter(
    path='CHECKPOINTS',
    auto_convert_markdown=True  # Auto-generate .md for GitHub
)

# Create checkpoint (dual format)
checkpoint.create(
    description="Week 1 Day 2 Complete",
    data={
        "timestamp": "2025-11-17T15:30:00Z",
        "tasks_completed": [
            {"task": "Create CLI tool", "status": "completed"},
            {"task": "Fix calculation bug", "status": "completed"},
        ],
        "metrics": {"commits": 3, "files_changed": 4}
    },
    format='dual',
    auto_commit=True
)

# Creates:
# - CHECKPOINTS/2025-11-17T15-30-00Z-week-1-day-2-complete.toon
# - CHECKPOINTS/2025-11-17T15-30-00Z-week-1-day-2-complete.md
# - Commits both to git
```

### Example 3: LLM Prompt Optimization

```python
from toon_module import LLMAdapter
import anthropic

# Initialize LLM adapter
llm = LLMAdapter(input_encoding=True, cache_enabled=True)

# Large checkpoint data (10,000 tokens in JSON)
checkpoint_data = load_checkpoint('2025-11-17-week1-day2')

# Encode for prompt (reduces to ~6,000 tokens)
optimized_prompt = llm.encode_for_prompt(checkpoint_data, format='auto')

# Send to Claude
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4",
    max_tokens=1024,
    messages=[
        llm.create_optimized_message("user", f"""
Review this checkpoint and provide next steps:

{optimized_prompt}
""")
    ]
)

# Get savings report
print(llm.get_savings_report())
# → Saved 4,000 tokens (40% reduction)
# → Estimated cost savings: $0.06
```

### Example 4: Configurable Toggle

```python
# Development: TOON enabled
export TOON_ENABLED=true
export TOON_STORAGE_FORMAT=dual

# Production: TOON disabled (rollback to JSON)
export TOON_ENABLED=false

# Code works unchanged!
from toon_module import encode

data = {"name": "test", "value": 123}

# Returns TOON if enabled, JSON if disabled
encoded = encode(data)  # Transparent switching
```

---

## Implementation Plan

### Phase 1: Core Module (Week 3, Days 1-2)
- [ ] Create module structure
- [ ] Implement base encoder/decoder interfaces
- [ ] Implement TOON encoder/decoder
- [ ] Add configuration system
- [ ] Unit tests (90% coverage)

### Phase 2: Adapters (Week 3, Days 3-4)
- [ ] StorageAdapter implementation
- [ ] LLMAdapter implementation
- [ ] CheckpointAdapter implementation
- [ ] Integration tests

### Phase 3: Converters (Week 3, Day 5)
- [ ] TOON ↔ Markdown converter
- [ ] TOON ↔ JSON converter
- [ ] Pre-commit hook setup
- [ ] Converter tests

### Phase 4: Integration (Week 4, Days 1-2)
- [ ] Integrate into deduplicator
- [ ] Integrate into checkpoint system
- [ ] Update CLI tools
- [ ] Backward compatibility tests

### Phase 5: Validation (Week 4, Days 3-5)
- [ ] Process historical data
- [ ] Measure token savings
- [ ] Performance benchmarking
- [ ] Documentation
- [ ] Production deployment

---

## Success Metrics

### Performance Targets
- **Token Reduction:** 35-45% on structured data
- **Processing Overhead:** <10ms per encode/decode
- **Memory Footprint:** <50MB cache
- **Backward Compatibility:** 100% (zero breaking changes)

### Quality Gates
- **Test Coverage:** ≥90%
- **Type Safety:** 100% (mypy strict mode)
- **Documentation:** All public APIs documented
- **Examples:** ≥5 real-world usage examples

### Business Metrics
- **Implementation Time:** 8 days (1 week)
- **Investment:** $2,400
- **Expected Annual Savings:** $14,000-$30,000
- **ROI:** 600-800%
- **Break-Even:** 1.5-2 months

---

## Risk Mitigation

### Risk 1: TOON Library Instability
**Mitigation:** Vendor TOON library, fork if needed, maintain our own encoder

### Risk 2: Format Lock-In
**Mitigation:** Dual-format storage, converters, fallback to JSON

### Risk 3: Performance Degradation
**Mitigation:** Lazy loading, caching, async encoding, benchmarks

### Risk 4: Breaking Changes
**Mitigation:** Feature flags, backward compatibility layer, gradual rollout

---

## Next Steps

1. **Review this spec** - Approve architecture and API design
2. **Budget allocation** - $2,400 for 1 week implementation
3. **Assign developer** - 1 full-stack Python developer
4. **Begin Phase 1** - Core module implementation (Week 3)

---

**Questions for Review:**

1. Does the modular architecture meet requirements?
2. Is the configuration system flexible enough?
3. Are the adapter patterns appropriate?
4. Should we add more converters (e.g., CSV, XML)?
5. Any concerns about backward compatibility?

---

**Status:** ✅ Ready for Review and Approval

