# Antivirus Software Troubleshooting

## Why Antivirus Software Flags Syllabo

Syllabo is packaged using PyInstaller, which creates standalone executables by bundling Python and all dependencies into a single file. This packaging method often triggers false positives in antivirus software because:

1. The executable contains compressed Python bytecode
2. It unpacks files to temporary directories at runtime
3. It exhibits behavior similar to some malware (self-extraction)

## This is NOT malware

Syllabo is open source software. You can:
- Review the complete source code on GitHub
- Build the executable yourself from source
- Verify the file checksums provided with releases

## Solutions by Antivirus Software

### Windows Defender
1. Open Windows Security
2. Go to "Virus & threat protection"
3. Click "Manage settings" under "Virus & threat protection settings"
4. Scroll to "Exclusions" and click "Add or remove exclusions"
5. Click "Add an exclusion" → "File"
6. Select the syllabo.exe file

### Norton Antivirus
1. Open Norton
2. Go to "Settings" → "Antivirus"
3. Click "Scans and Risks" → "Exclusions/Low Risks"
4. Click "Configure" next to "Items to Exclude from Scans"
5. Add the syllabo.exe file

### McAfee
1. Open McAfee Security Center
2. Go to "Virus and Spyware Protection"
3. Click "Real-Time Scanning"
4. Click "Excluded Files"
5. Add the syllabo.exe file

### Avast/AVG
1. Open Avast/AVG
2. Go to "Settings" → "General" → "Exceptions"
3. Click "Add Exception"
4. Browse to and select syllabo.exe

### Bitdefender
1. Open Bitdefender
2. Go to "Protection" → "Antivirus"
3. Click "Settings" → "Manage Exceptions"
4. Add the syllabo.exe file

## Alternative Solutions

### Download from Official Source
Always download from the official GitHub releases page:
https://github.com/PixelCode01/syllabo/releases

### Verify File Integrity
Check the SHA256 hash of the downloaded file against the provided checksum.

### Build from Source
If you're comfortable with Python development:
```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
pip install -r requirements.txt
python main.py
```

### Use Python Installation
Instead of the standalone executable:
```bash
pip install -r requirements.txt
python main.py
```

## For IT Administrators

### Group Policy Exclusions
Add exclusions through Group Policy for enterprise deployments:
1. Open Group Policy Management Console
2. Navigate to Computer Configuration → Administrative Templates → Windows Components → Windows Defender Antivirus → Exclusions
3. Add file exclusions for syllabo.exe

### Enterprise Antivirus Solutions
Most enterprise antivirus solutions allow administrators to:
- Whitelist specific file hashes
- Create exclusions based on file paths
- Submit files for analysis and whitelisting

## Reporting False Positives

Help improve detection by reporting false positives:

### Windows Defender
Submit files at: https://www.microsoft.com/en-us/wdsi/filesubmission

### Other Vendors
Most antivirus vendors have online submission forms for false positive reports.

## Technical Details

### Why This Happens
PyInstaller executables:
- Contain compressed Python interpreter and libraries
- Extract files to temporary directories at runtime
- Use techniques that can appear suspicious to heuristic scanners

### File Information
- File Type: Windows PE32 executable
- Packer: PyInstaller
- Language: Python
- Dependencies: Bundled (no external requirements)

## Still Having Issues?

If you continue to experience problems:
1. Check our GitHub issues page
2. Contact your IT administrator
3. Consider using the Python source version instead

The software is completely safe and open source. The detection is a false positive caused by the packaging method, not malicious code.