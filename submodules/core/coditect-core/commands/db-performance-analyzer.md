# Database Performance Analyzer Command

## Description
Advanced database performance analysis and optimization command for SQL and NoSQL systems. Provides comprehensive query analysis, index optimization recommendations, and performance tuning strategies for enterprise database architectures.

## Usage
```bash
/db-performance-analyzer [database-type] [analysis-scope] [optimization-level]
```

## Parameters
- `database-type`: postgresql | mysql | redis | mongodb | foundationdb
- `analysis-scope`: queries | indexes | connections | full-system
- `optimization-level`: basic | advanced | enterprise

## Command Implementation

### Query Performance Analysis
```sql
-- PostgreSQL performance analysis queries
-- Slow query identification
SELECT 
    query,
    mean_time,
    calls,
    total_time,
    (total_time / calls) as avg_time_ms,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements 
WHERE mean_time > 1000 -- queries slower than 1 second
ORDER BY total_time DESC 
LIMIT 20;

-- Index usage analysis
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as size
FROM pg_stat_user_indexes 
WHERE idx_scan < 100 -- potentially unused indexes
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Table bloat analysis
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) as index_size
FROM pg_stat_user_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Index Optimization Recommendations
```yaml
index_analysis:
  postgresql:
    missing_indexes:
      - table: "users"
        columns: ["tenant_id", "email"]
        rationale: "High cardinality composite key for multi-tenant queries"
        impact: "90% query performance improvement"
        
    unused_indexes:
      - index: "idx_users_created_at"
        size: "2.5GB"
        usage: "0 scans in 30 days"
        recommendation: "DROP - reclaim storage space"
        
    partial_index_opportunities:
      - table: "sessions"
        condition: "WHERE active = true AND expires_at > NOW()"
        benefit: "75% index size reduction"
        
  mongodb:
    compound_index_optimization:
      - collection: "events"
        current: ["tenant_id", "event_type", "created_at"]
        optimized: ["tenant_id", "created_at", "event_type"]
        rationale: "Sort field should be last for range queries"
        
  redis:
    memory_optimization:
      - data_structure: "hash"
        current_memory: "1.2GB"
        optimized_memory: "800MB"
        strategy: "Use smaller hash max entries"
```

### Connection Pool Analysis
```rust
// Connection pool performance analysis
use sqlx::{PgPool, Row};

pub struct ConnectionPoolAnalyzer {
    pool: PgPool,
}

impl ConnectionPoolAnalyzer {
    pub async fn analyze_pool_performance(&self) -> Result<PoolAnalysis, sqlx::Error> {
        let stats = sqlx::query(r#"
            SELECT 
                numbackends,
                xact_commit + xact_rollback as total_transactions,
                xact_commit,
                xact_rollback,
                blks_read,
                blks_hit,
                100.0 * blks_hit / (blks_hit + blks_read) as cache_hit_ratio,
                tup_returned,
                tup_fetched,
                tup_inserted,
                tup_updated,
                tup_deleted,
                conflicts,
                temp_files,
                temp_bytes
            FROM pg_stat_database 
            WHERE datname = current_database()
        "#).fetch_one(&self.pool).await?;
        
        let cache_hit_ratio: f64 = stats.get("cache_hit_ratio");
        let active_connections: i32 = stats.get("numbackends");
        
        let recommendations = self.generate_recommendations(
            cache_hit_ratio,
            active_connections,
        );
        
        Ok(PoolAnalysis {
            cache_hit_ratio,
            active_connections,
            recommendations,
        })
    }
    
    fn generate_recommendations(&self, cache_hit_ratio: f64, connections: i32) -> Vec<String> {
        let mut recommendations = Vec::new();
        
        if cache_hit_ratio < 95.0 {
            recommendations.push(format!(
                "Cache hit ratio is {:.1}%. Consider increasing shared_buffers to improve performance.",
                cache_hit_ratio
            ));
        }
        
        if connections > 80 {
            recommendations.push(format!(
                "High connection count ({}). Consider implementing connection pooling with PgBouncer.",
                connections
            ));
        }
        
        recommendations
    }
}

pub struct PoolAnalysis {
    pub cache_hit_ratio: f64,
    pub active_connections: i32,
    pub recommendations: Vec<String>,
}
```

## Output Format

### Performance Report Structure
```json
{
  "database_type": "postgresql",
  "analysis_timestamp": "2024-11-07T10:30:00Z",
  "performance_score": 85,
  "critical_issues": [
    {
      "type": "slow_query",
      "query_hash": "abc123",
      "avg_execution_time": 2500,
      "calls_per_minute": 45,
      "optimization_recommendation": "Add composite index on (tenant_id, created_at)"
    }
  ],
  "optimization_opportunities": [
    {
      "type": "index_optimization",
      "table": "users",
      "current_size": "1.2GB",
      "optimized_size": "800MB",
      "performance_improvement": "40%"
    }
  ],
  "resource_utilization": {
    "cpu_usage": 65,
    "memory_usage": 78,
    "disk_io": 320,
    "connection_pool": 45
  }
}
```

## Integration with Database-Architect Agent

### Automated Performance Analysis
```yaml
workflow_integration:
  trigger: "schema_change_detection"
  analysis_types: ["query_performance", "index_efficiency", "resource_utilization"]
  
  performance_thresholds:
    query_time_warning: 1000  # ms
    query_time_critical: 5000  # ms
    cache_hit_ratio_min: 95.0  # %
    connection_pool_max: 80  # connections
    
  optimization_automation:
    auto_create_indexes: false  # requires approval
    auto_analyze_tables: true
    auto_vacuum_tuning: true
    alert_on_degradation: true
```

### Multi-Database Support
```yaml
database_configurations:
  postgresql:
    performance_views: ["pg_stat_statements", "pg_stat_user_indexes", "pg_stat_database"]
    optimization_focus: ["query_plans", "index_usage", "vacuum_stats"]
    
  mysql:
    performance_schema: ["events_statements_summary_by_digest", "table_io_waits_summary_by_index_usage"]
    optimization_focus: ["slow_query_log", "index_statistics", "buffer_pool"]
    
  mongodb:
    profiling_level: 2  # profile all operations
    optimization_focus: ["index_stats", "operation_profiling", "collection_stats"]
    
  redis:
    info_sections: ["memory", "stats", "keyspace", "replication"]
    optimization_focus: ["memory_usage", "key_distribution", "command_stats"]
```

## Examples

### Basic Performance Analysis
```bash
/db-performance-analyzer postgresql queries basic
```

### Comprehensive System Analysis
```bash
/db-performance-analyzer foundationdb full-system enterprise
```

### Index Optimization Focus
```bash
/db-performance-analyzer mysql indexes advanced
```

## Success Criteria
- Query performance improvements of 25-50%
- Index optimization reducing storage by 10-30%
- Connection pool efficiency improvements of 15-25%
- Automated detection of performance regressions
- Actionable optimization recommendations with impact estimates