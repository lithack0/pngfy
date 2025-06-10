# Pngfy

A Python script that validates PNG files by checking their hex signatures and automatically repairs corrupted headers/footers.

## Features

- ✅ **True PNG Detection**: Identifies PNG files by header signature, not file extension
- 🔍 **Hex Signature Validation**: Checks both header (first 16 bytes) and footer (last 12 bytes)
- 🔧 **Automatic Repair**: Fixes corrupted PNG signatures with proper hex values
- 💾 **Safe Operation**: Creates backups before making any changes
- 📊 **Detailed Reporting**: Shows exactly what was found and what was fixed
- 🔄 **Verification**: Re-validates files after repair to ensure success

## Installation

### Method 1: Clone from GitHub

```bash
git clone https://github.com/yourusername/png-validator.git
cd png-validator
```

### Method 2: Direct Download

Download the `png_validator.py` file directly from the repository.

### Requirements

- Python 3.6 or higher
- No external dependencies (uses only built-in Python libraries)

## Usage

### Basic Usage

```bash
python png_validator.py <path_to_file>
```

### Examples

```bash
# Validate a PNG file
python png_validator.py image.png

# Works with any file extension (detects PNG by header)
python png_validator.py suspicious_file.txt

# Validate and repair a corrupted PNG
python png_validator.py corrupted_image.png
```

### Command Line Help

```bash
python png_validator.py
```

This will display usage instructions.

## How It Works

### PNG Signature Detection

The script validates PNG files using their binary signatures:

- **Header Signature** (first 8 bytes): `89 50 4E 47 0D 0A 1A 0A`
- **Complete Header** (first 16 bytes): `89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52`
- **Footer Signature** (last 12 bytes): `00 00 00 00 49 45 4E 44 AE 42 60 82`

### Validation Process

1. **File Reading**: Reads the entire file as binary data
2. **Format Detection**: Checks if file is PNG by examining header signature
3. **Header Validation**: Compares first 16 bytes with expected PNG header
4. **Footer Validation**: Compares last 12 bytes with expected PNG footer
5. **Repair (if needed)**: Corrects any corrupted signatures
6. **Backup Creation**: Saves original file as `.backup` before repairs
7. **Verification**: Re-validates the repaired file

## Output Examples

### Valid PNG File

```
============================================================
PNG File Validator and Repairer
============================================================
Processing file: valid_image.png
✅ File identified as PNG by header signature
📁 File size: 125847 bytes

🔍 Checking PNG signatures...
✅ Header is valid
✅ Footer is valid

✅ PNG file is not corrupted - no repair needed

🎉 Processing completed successfully!
```

### Corrupted PNG File (Before Repair)

```
============================================================
PNG File Validator and Repairer
============================================================
Processing file: corrupted_image.png
✅ File identified as PNG by header signature
📁 File size: 89234 bytes

🔍 Checking PNG signatures...
❌ Header corrupted!
   Current:  89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 00
   Expected: 89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52
✅ Footer is valid

🔧 Repairing PNG file...
✅ Header repaired
💾 Backup created: corrupted_image.png.backup
✅ File repaired successfully: corrupted_image.png

🔄 Verifying repair...
Processing file: corrupted_image.png
✅ File identified as PNG by header signature
📁 File size: 89234 bytes

🔍 Checking PNG signatures...
✅ Header is valid
✅ Footer is valid

✅ PNG file is not corrupted - no repair needed

🎉 Processing completed successfully!
```

### Non-PNG File

```
============================================================
PNG File Validator and Repairer
============================================================
Processing file: document.pdf
❌ File is not a PNG file (invalid header signature)
   File header: 25 50 44 46 2D 31 2E 34
   PNG signature: 89 50 4E 47 0D 0A 1A 0A

❌ Processing failed!
```

## File Safety

- **Automatic Backups**: Original files are backed up as `filename.backup` before any modifications
- **Non-destructive**: Only repairs known corruption patterns
- **Verification**: All repairs are verified before completion

## Technical Details

### PNG File Structure

PNG files have a specific binary structure:

```
[PNG Signature - 8 bytes]
[IHDR Chunk - 8 bytes header + data]
[... other chunks ...]
[IEND Chunk - 12 bytes]
```

The script specifically validates:
- PNG file signature (first 8 bytes)
- Complete IHDR chunk header (bytes 1-16)
- IEND chunk (last 12 bytes)

### Supported Repairs

- Corrupted PNG file signature
- Corrupted IHDR chunk header
- Corrupted IEND chunk footer
- Mixed corruption scenarios

## Troubleshooting

### Common Issues

**"File does not exist"**
- Check the file path is correct
- Ensure you have read permissions

**"File too small to be a valid PNG"**
- File must be at least 28 bytes (minimum PNG structure)
- File might be completely corrupted or not a PNG

**"Error reading file"**
- Check file permissions
- Ensure file is not locked by another application

### Getting Help

If you encounter issues:

1. Check that you're using Python 3.6+
2. Verify file permissions
3. Ensure the file path is correct
4. Look at the detailed error messages in the output

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0
- Initial release
- PNG signature validation
- Automatic repair functionality
- Backup creation
- Header-based PNG detection

---

## Author's Note 💝

Hey there, fellow developers and digital explorers! 👋

I created this little PNG validator with a lot of love and countless cups of coffee ☕. Having dealt with corrupted image files more times than I'd like to admit, I know how frustrating it can be when a perfectly good image suddenly becomes "unreadable" due to a few flipped bits in the header or footer.

This tool was born out of necessity and refined with patience. I hope it saves you the headache I've experienced when dealing with corrupted PNG files. Whether you're a forensics expert, a developer debugging image processing pipelines, or just someone who stumbled upon a broken PNG file, I hope this script serves you well.

Remember: every byte tells a story, and sometimes we just need to help it tell the right one! 🔍✨

Keep coding, keep exploring, and never stop being curious about the beautiful complexity hiding in our digital world.

With binary love and hexadecimal hugs,  
**117h4ck** 💻

*P.S. - If this tool helped you save a precious memory trapped in a corrupted PNG, that makes all the late-night debugging sessions worth it! 🌟*

---

**Technical Note**: This tool is designed for PNG files that have corrupted signatures but are otherwise structurally sound. It cannot repair PNG files with damaged image data or severely corrupted internal structures.
