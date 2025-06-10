#!/usr/bin/env python3
"""
Pngfy 

This script validates PNG files by checking their hex signatures and repairs
corrupted headers/footers if needed.
"""

import os
import sys
from pathlib import Path

def is_png_file(file_data):
    """Check if the file is a PNG by examining the header bytes"""
    if len(file_data) < 8:
        return False
    
    # PNG signature: 89 50 4E 47 0D 0A 1A 0A (first 8 bytes)
    png_signature = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
    return file_data[:8] == png_signature

def read_file_as_hex(file_path):
    """Read file and return its content as bytes"""
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def write_file_from_bytes(file_path, data):
    """Write bytes data to file"""
    try:
        with open(file_path, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False

def validate_and_repair_png(file_path):
    """
    Validate PNG file and repair if corrupted
    
    PNG Header (first 16 bytes): 89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52
    PNG Footer (last 12 bytes):  00 00 00 00 49 45 4E 44 AE 42 60 82
    """
    
    # Expected signatures
    expected_header = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 
                           0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52])
    expected_footer = bytes([0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 
                           0xAE, 0x42, 0x60, 0x82])
    
    print(f"Processing file: {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print("❌ File does not exist")
        return False
    
    # Read file content
    file_data = read_file_as_hex(file_path)
    if file_data is None:
        return False
    
    # Check if file is PNG by header signature
    if not is_png_file(file_data):
        print("❌ File is not a PNG file (invalid header signature)")
        print(f"   File header: {' '.join(f'{b:02X}' for b in file_data[:8]) if len(file_data) >= 8 else 'Too short'}")
        print(f"   PNG signature: 89 50 4E 47 0D 0A 1A 0A")
        return False
    
    print("✅ File identified as PNG by header signature")
    
    file_size = len(file_data)
    print(f"📁 File size: {file_size} bytes")
    
    if file_size < 28:  # Minimum size for header + footer
        print("❌ File too small to be a valid PNG")
        return False
    
    # Extract current header and footer
    current_header = file_data[:16]
    current_footer = file_data[-12:]
    
    print("\n🔍 Checking PNG signatures...")
    
    # Check header
    header_corrupted = current_header != expected_header
    if header_corrupted:
        print("❌ Header corrupted!")
        print(f"   Current:  {' '.join(f'{b:02X}' for b in current_header)}")
        print(f"   Expected: {' '.join(f'{b:02X}' for b in expected_header)}")
    else:
        print("✅ Header is valid")
    
    # Check footer
    footer_corrupted = current_footer != expected_footer
    if footer_corrupted:
        print("❌ Footer corrupted!")
        print(f"   Current:  {' '.join(f'{b:02X}' for b in current_footer)}")
        print(f"   Expected: {' '.join(f'{b:02X}' for b in expected_footer)}")
    else:
        print("✅ Footer is valid")
    
    # Repair if needed
    if header_corrupted or footer_corrupted:
        print("\n🔧 Repairing PNG file...")
        
        # Create repaired data
        repaired_data = bytearray(file_data)
        
        # Fix header
        if header_corrupted:
            repaired_data[:16] = expected_header
            print("✅ Header repaired")
        
        # Fix footer
        if footer_corrupted:
            repaired_data[-12:] = expected_footer
            print("✅ Footer repaired")
        
        # Create backup
        backup_path = f"{file_path}.backup"
        if write_file_from_bytes(backup_path, file_data):
            print(f"💾 Backup created: {backup_path}")
        
        # Write repaired file
        if write_file_from_bytes(file_path, bytes(repaired_data)):
            print(f"✅ File repaired successfully: {file_path}")
            
            # Verify repair
            print("\n🔄 Verifying repair...")
            return validate_and_repair_png(file_path)
        else:
            print("❌ Failed to write repaired file")
            return False
    else:
        print("\n✅ PNG file is not corrupted - no repair needed")
        return True

def print_hex_dump(data, start_offset=0, length=32):
    """Print hex dump of data"""
    for i in range(0, min(length, len(data)), 16):
        hex_part = ' '.join(f'{b:02X}' for b in data[i:i+16])
        ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data[i:i+16])
        print(f"{start_offset + i:08X}: {hex_part:<48} {ascii_part}")

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python png_validator.py <path_to_file>")
        print("Example: python png_validator.py image.png")
        print("Note: File extension doesn't matter - PNG format is detected by header signature")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print("=" * 60)
    print("PNG File Validator and Repairer")
    print("=" * 60)
    
    success = validate_and_repair_png(file_path)
    
    if success:
        print(f"\n🎉 Processing completed successfully!")
    else:
        print(f"\n❌ Processing failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
