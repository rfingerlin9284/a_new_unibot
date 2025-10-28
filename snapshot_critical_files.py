#!/usr/bin/env python3
"""
Critical Files Snapshot Tool for Live Trading Bot

This script identifies, validates, and creates snapshots of all critical files
needed for live real money trading operations.
"""

import json
import os
import shutil
import glob
import datetime
import hashlib
import zipfile
import logging
from pathlib import Path
from typing import List, Dict, Set, Tuple
from common_utils import (
    ensure_directory_exists,
    write_file_safely,
    get_timestamp,
    load_json_config,
    setup_logger
)

class CriticalFilesSnapshot:
    """
    Manages identification and snapshotting of critical files for live trading.
    """
    
    def __init__(self, config_path: str = "critical_files_config.json"):
        """Initialize with configuration file."""
        self.config_path = config_path
        self.config = load_json_config(config_path)
        self.logger = setup_logger(__name__, 'critical_files_snapshot.log')
        
    def identify_critical_files(self) -> Dict[str, List[str]]:
        """
        Identify all critical files based on configuration patterns.
        
        Returns:
            Dictionary mapping categories to lists of found files
        """
        self.logger.info("Starting critical file identification...")
        critical_files = {}
        
        categories = self.config['critical_files_definition']['categories']
        
        for category_name, category_config in categories.items():
            self.logger.info(f"Scanning category: {category_name}")
            found_files = []
            
            for pattern in category_config['patterns']:
                # Use glob to find files matching the pattern
                matches = glob.glob(pattern, recursive=True)
                found_files.extend([f for f in matches if os.path.isfile(f)])
            
            # Remove duplicates while preserving order
            found_files = list(dict.fromkeys(found_files))
            critical_files[category_name] = found_files
            
            self.logger.info(f"Found {len(found_files)} files in {category_name}")
            
            # Check if required category has files
            if category_config.get('required', False) and not found_files:
                self.logger.warning(f"Required category '{category_name}' has no files!")
        
        return critical_files
    
    def validate_critical_files(self, critical_files: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Validate critical files for integrity and accessibility.
        
        Args:
            critical_files: Dictionary of categorized critical files
            
        Returns:
            Dictionary of validation results
        """
        self.logger.info("Validating critical files...")
        validation_results = {}
        
        for category, files in critical_files.items():
            category_results = []
            
            for file_path in files:
                result = {
                    'file': file_path,
                    'exists': os.path.exists(file_path),
                    'readable': False,
                    'size': 0,
                    'checksum': None
                }
                
                if result['exists']:
                    try:
                        # Check if file is readable
                        with open(file_path, 'rb') as f:
                            content = f.read()
                            result['readable'] = True
                            result['size'] = len(content)
                            result['checksum'] = hashlib.md5(content).hexdigest()
                    except (PermissionError, IOError) as e:
                        self.logger.warning(f"Cannot read file {file_path}: {e}")
                
                category_results.append(result)
            
            validation_results[category] = category_results
        
        return validation_results
    
    def create_snapshot(self, critical_files: Dict[str, List[str]]) -> str:
        """
        Create a snapshot of all critical files.
        
        Args:
            critical_files: Dictionary of categorized critical files
            
        Returns:
            Path to created snapshot
        """
        timestamp = get_timestamp(
            self.config['snapshot_settings']['timestamp_format']
        )
        
        snapshot_dir = f"{self.config['snapshot_settings']['snapshot_directory']}_{timestamp}"
        
        self.logger.info(f"Creating snapshot in {snapshot_dir}")
        
        # Create snapshot directory
        ensure_directory_exists(snapshot_dir)
        
        # Copy files to snapshot directory maintaining structure
        for category, files in critical_files.items():
            category_dir = os.path.join(snapshot_dir, category)
            ensure_directory_exists(category_dir)
            
            for file_path in files:
                if os.path.exists(file_path):
                    # Create subdirectory structure if needed
                    relative_path = os.path.relpath(file_path)
                    dest_path = os.path.join(category_dir, relative_path)
                    dest_dir = os.path.dirname(dest_path)
                    
                    ensure_directory_exists(dest_dir)
                    
                    try:
                        shutil.copy2(file_path, dest_path)
                        self.logger.debug(f"Copied {file_path} to {dest_path}")
                    except (PermissionError, IOError) as e:
                        self.logger.error(f"Failed to copy {file_path}: {e}")
        
        # Create manifest file
        manifest = {
            'timestamp': timestamp,
            'total_files': sum(len(files) for files in critical_files.values()),
            'categories': critical_files,
            'config_version': self.config['critical_files_definition']['version']
        }
        
        manifest_path = os.path.join(snapshot_dir, 'snapshot_manifest.json')
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Compress if enabled
        if self.config['snapshot_settings'].get('compression', False):
            zip_path = f"{snapshot_dir}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(snapshot_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, snapshot_dir)
                        zipf.write(file_path, arcname)
            
            # Remove uncompressed directory
            shutil.rmtree(snapshot_dir)
            self.logger.info(f"Compressed snapshot created: {zip_path}")
            return zip_path
        
        self.logger.info(f"Snapshot created: {snapshot_dir}")
        return snapshot_dir
    
    def generate_report(self, critical_files: Dict[str, List[str]], 
                       validation_results: Dict[str, List[str]]) -> str:
        """
        Generate a comprehensive report of the snapshot operation.
        
        Args:
            critical_files: Dictionary of categorized critical files
            validation_results: Validation results for the files
            
        Returns:
            Path to generated report
        """
        timestamp = get_timestamp("%Y%m%d_%H%M%S")
        report_path = f"critical_files_report_{timestamp}.md"
        
        with open(report_path, 'w') as f:
            f.write("# Critical Files Snapshot Report\n\n")
            f.write(f"**Generated:** {datetime.datetime.now().isoformat()}\n")
            f.write(f"**Configuration Version:** {self.config['critical_files_definition']['version']}\n\n")
            
            # Summary
            total_files = sum(len(files) for files in critical_files.values())
            f.write(f"## Summary\n\n")
            f.write(f"- **Total Critical Files:** {total_files}\n")
            f.write(f"- **Categories Scanned:** {len(critical_files)}\n\n")
            
            # Categories breakdown
            f.write("## Categories Breakdown\n\n")
            for category, files in critical_files.items():
                category_config = self.config['critical_files_definition']['categories'][category]
                f.write(f"### {category.replace('_', ' ').title()}\n\n")
                f.write(f"**Description:** {category_config['description']}\n")
                f.write(f"**Required:** {'Yes' if category_config.get('required', False) else 'No'}\n")
                f.write(f"**Files Found:** {len(files)}\n\n")
                
                if files:
                    f.write("**Files:**\n")
                    for file_path in files:
                        f.write(f"- `{file_path}`\n")
                else:
                    f.write("⚠️ **No files found for this category**\n")
                f.write("\n")
            
            # Validation results
            f.write("## Validation Results\n\n")
            for category, results in validation_results.items():
                f.write(f"### {category.replace('_', ' ').title()}\n\n")
                if results:
                    f.write("| File | Exists | Readable | Size | Checksum |\n")
                    f.write("|------|--------|----------|------|----------|\n")
                    for result in results:
                        status = "✅" if result['exists'] and result['readable'] else "❌"
                        f.write(f"| {result['file']} | {status} | {result['readable']} | {result['size']} bytes | {result['checksum'][:8] if result['checksum'] else 'N/A'} |\n")
                else:
                    f.write("No files to validate in this category.\n")
                f.write("\n")
        
        self.logger.info(f"Report generated: {report_path}")
        return report_path
    
    def run_snapshot(self) -> Tuple[str, str]:
        """
        Execute complete snapshot process.
        
        Returns:
            Tuple of (snapshot_path, report_path)
        """
        self.logger.info("Starting critical files snapshot process...")
        
        try:
            # Identify critical files
            critical_files = self.identify_critical_files()
            
            # Validate files
            validation_results = self.validate_critical_files(critical_files)
            
            # Create snapshot
            snapshot_path = self.create_snapshot(critical_files)
            
            # Generate report
            report_path = self.generate_report(critical_files, validation_results)
            
            self.logger.info("Snapshot process completed successfully!")
            return snapshot_path, report_path
            
        except Exception as e:
            self.logger.error(f"Snapshot process failed: {e}")
            raise


def main():
    """Main entry point for the script."""
    try:
        snapshot_tool = CriticalFilesSnapshot()
        snapshot_path, report_path = snapshot_tool.run_snapshot()
        
        print(f"\n✅ Critical files snapshot completed!")
        print(f"📂 Snapshot: {snapshot_path}")
        print(f"📋 Report: {report_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())