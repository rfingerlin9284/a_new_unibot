# Critical Files Preservation System

This system identifies, validates, and creates snapshots of all critical files needed for live real money trading operations.

## Overview

The Critical Files Preservation System ensures that all essential components of your trading bot are properly identified, validated, and backed up before live trading operations. This is crucial for:

- **Risk Management**: Ensuring all safety mechanisms are in place
- **Disaster Recovery**: Quick restoration of trading operations
- **Compliance**: Maintaining records of trading system state
- **Debugging**: Analyzing system state during issues

## Components

### 1. Configuration (`critical_files_config.json`)
Defines what constitutes critical files across different categories:
- **Core Trading**: Strategy and algorithm files
- **Configuration**: API keys, trading parameters, risk settings
- **Risk Management**: Stop-loss, position sizing, portfolio management
- **Data Handling**: Market data, database components
- **Monitoring & Logging**: System monitoring and event logging
- **Testing & Validation**: Gold standard tests and validation frameworks
- **Deployment**: Environment and deployment configurations

### 2. Snapshot Tool (`snapshot_critical_files.py`)
Python script that:
- Scans for critical files based on configuration patterns
- Validates file integrity and accessibility
- Creates timestamped snapshots with organized structure
- Generates comprehensive reports
- Supports compression and retention policies

### 3. Sample Files Generator (`create_sample_files.py`)
Creates sample trading bot files for testing and demonstration.

## Usage

### Quick Start

1. **Create sample files for testing** (optional):
   ```bash
   python create_sample_files.py
   ```

2. **Run the critical files snapshot**:
   ```bash
   python snapshot_critical_files.py
   ```

3. **Review the generated report and snapshot**:
   - Snapshot directory: `live_snapshot_YYYYMMDD_HHMMSS/`
   - Report file: `critical_files_report_YYYYMMDD_HHMMSS.md`

### Configuration

Edit `critical_files_config.json` to customize:

```json
{
  "critical_files_definition": {
    "categories": {
      "core_trading": {
        "patterns": ["src/strategies/**/*.py", "main_trading.py"],
        "required": true
      }
    }
  },
  "snapshot_settings": {
    "compression": true,
    "retention_days": 30
  }
}
```

### File Patterns

The system uses glob patterns to identify files:
- `**/*.py` - All Python files recursively
- `config/*.json` - All JSON files in config directory
- `src/strategies/**/*.py` - All Python files in strategies subdirectories

## Critical File Categories

### Core Trading Files ⚠️ **CRITICAL**
- Trading strategies and algorithms
- Main trading bot entry points
- Strategy execution logic

### Configuration Files ⚠️ **CRITICAL** 🔒 **SENSITIVE**
- API keys and credentials
- Trading parameters
- Risk management settings
- Environment variables

### Risk Management ⚠️ **CRITICAL**
- Stop-loss mechanisms
- Position sizing algorithms
- Portfolio management logic
- Emergency shutdown procedures

### Data Components ⚠️ **CRITICAL**
- Market data handlers
- Database connections
- Data validation logic
- Price feed integrations

### Monitoring & Logging ⚠️ **CRITICAL**
- Trade execution logging
- System health monitoring
- Alert mechanisms
- Performance tracking

### Testing Framework ⚠️ **CRITICAL**
- Integration tests
- Live trading validation
- Gold standard test suites
- Backtesting frameworks

## Security Considerations

⚠️ **WARNING**: Critical files may contain sensitive information:
- API keys and secrets
- Trading strategies (intellectual property)
- Configuration parameters

### Best Practices:
1. **Encrypt snapshots** containing sensitive data
2. **Secure storage** for backup files
3. **Access control** for snapshot directories
4. **Regular rotation** of API keys
5. **Audit trails** for snapshot access

## Automation

### Scheduled Snapshots
Set up cron job for regular snapshots:
```bash
# Daily snapshot at 2 AM
0 2 * * * cd /path/to/trading/bot && python snapshot_critical_files.py
```

### Pre-deployment Checks
Always run snapshot before deploying:
```bash
python snapshot_critical_files.py && echo "✅ Critical files snapshot complete - safe to deploy"
```

## Validation Rules

The system validates:
- ✅ File existence and accessibility
- ✅ File integrity (checksums)
- ✅ Required categories have files
- ✅ Configuration syntax validity
- ✅ Import statements in Python files

## Disaster Recovery

In case of system failure:

1. **Identify latest snapshot**:
   ```bash
   ls -la live_snapshot_* | tail -1
   ```

2. **Extract snapshot** (if compressed):
   ```bash
   unzip live_snapshot_YYYYMMDD_HHMMSS.zip
   ```

3. **Restore files**:
   ```bash
   cp -r live_snapshot_YYYYMMDD_HHMMSS/* ./
   ```

4. **Validate restoration**:
   ```bash
   python snapshot_critical_files.py
   ```

## Troubleshooting

### Common Issues

**No files found for required category**:
- Check file patterns in configuration
- Verify file paths and naming conventions
- Ensure files exist in expected locations

**Permission errors during snapshot**:
- Check file/directory permissions
- Ensure write access to snapshot directory
- Verify sufficient disk space

**Import errors in validation**:
- Check Python dependencies
- Verify PYTHONPATH configuration
- Ensure all required modules are installed

## Integration with Trading Bot

Add to your main trading bot:

```python
from snapshot_critical_files import CriticalFilesSnapshot

def pre_trading_checks():
    """Run before starting live trading."""
    snapshot_tool = CriticalFilesSnapshot()
    critical_files = snapshot_tool.identify_critical_files()
    
    # Ensure all critical categories have files
    required_categories = ['core_trading', 'configuration', 'risk_management']
    for category in required_categories:
        if not critical_files.get(category):
            raise RuntimeError(f"Missing critical files for {category}")
    
    # Create pre-trading snapshot
    snapshot_path, report_path = snapshot_tool.run_snapshot()
    logging.info(f"Pre-trading snapshot created: {snapshot_path}")
```

## License

This critical files preservation system is part of the a_new_unibot project.