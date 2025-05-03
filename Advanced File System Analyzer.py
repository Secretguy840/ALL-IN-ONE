import os
import hashlib
from collections import defaultdict
import csv
from datetime import datetime

class FileSystemAnalyzer:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.file_types = defaultdict(int)
        self.duplicates = defaultdict(list)
        self.stats = {
            'total_files': 0,
            'total_size': 0,
            'start_time': None,
            'end_time': None
        }

    def calculate_hash(self, filepath):
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def analyze(self):
        self.stats['start_time'] = datetime.now()
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    size = os.path.getsize(filepath)
                    _, ext = os.path.splitext(file)
                    
                    self.file_types[ext.lower()] += 1
                    self.stats['total_files'] += 1
                    self.stats['total_size'] += size
                    
                    file_hash = self.calculate_hash(filepath)
                    self.duplicates[file_hash].append(filepath)
                except (OSError, PermissionError) as e:
                    continue
        
        self.duplicates = {k: v for k, v in self.duplicates.items() if len(v) > 1}
        self.stats['end_time'] = datetime.now()

    def generate_report(self, output_file):
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['File Type', 'Count'])
            for ext, count in sorted(self.file_types.items()):
                writer.writerow([ext, count])
            
            writer.writerow([])
            writer.writerow(['Duplicate Files', 'Count'])
            for hash_val, files in self.duplicates.items():
                writer.writerow([f"Hash: {hash_val[:8]}...", len(files)])
                for file in files:
                    writer.writerow(['', file])
            
            writer.writerow([])
            writer.writerow(['Statistics', 'Value'])
            writer.writerow(['Total Files', self.stats['total_files']])
            writer.writerow(['Total Size (MB)', self.stats['total_size'] / (1024*1024)])
            writer.writerow(['Analysis Duration', 
                           (self.stats['end_time'] - self.stats['start_time'])])

# Usage
analyzer = FileSystemAnalyzer('/path/to/directory')
analyzer.analyze()
analyzer.generate_report('analysis_report.csv')
