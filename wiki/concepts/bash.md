---
title: Bash
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [bash, shell, scripting, command-line, terminal]
---

# Bash

## Overview

Bash (Bourne Again Shell) is a Unix command interpreter and scripting language that serves as the primary interface to the Unix/Linux operating system. It is the default shell on most Linux distributions and macOS (though macOS migrated to Zsh as default in Catalina). Bash extends the earlier Bourne shell (sh) with features from other shells like csh and ksh, making it one of the most powerful and widely deployed shells in existence.

Bash operates in a read-evaluate-print loop (REPL): it reads commands from the terminal or from script files, evaluates them, and prints the results. Beyond simple command execution, Bash provides variables, functions, control flow (if/else, loops, case statements), arithmetic operations, arrays, and robust string manipulation. These features transform Bash from a simple command launcher into a full programming language well-suited for system administration, task automation, and build pipeline scripting.

## Key Concepts

**Command Execution**: Bash parses input into words separated by whitespace. The first word is the command to execute; subsequent words are arguments. Special characters like `|`, `>`, `<`, and `&` have syntactic meaning for redirection and background execution.

```bash
# Simple command
ls -la /tmp

# Pipe: connect stdout of left to stdin of right
ps aux | grep python

# Redirection: capture output to file
make > build.log 2>&1

# Background execution
./long_running_script.sh &
```

**Variables**: Bash variables are untyped by default and store strings. Access by prefixing with `$`. Environment variables are exported to child processes.

```bash
NAME="Alice"
AGE=30
echo "Hello, $NAME"

# Arrays
files=("report.txt" "data.csv" "notes.md")
echo "${files[0]}"  # First element
echo "${files[@]}"   # All elements
```

**Functions**: Functions encapsulate reusable code blocks. They accept arguments as positional parameters (`$1`, `$2`, etc.) and can return status codes.

```bash
backup_dir() {
    local src="$1"
    local dest="$2"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    
    cp -r "$src" "$dest/backup_${timestamp}"
    return $?
}

backup_dir "/home/user/docs" "/mnt/backups"
```

**Control Flow**: Bash provides standard branching and looping constructs.

```bash
# If-elif-else
if [[ $age -lt 18 ]]; then
    echo "Minor"
elif [[ $age -lt 65 ]]; then
    echo "Adult"
else
    echo "Senior"
fi

# For loop over items
for file in *.txt; do
    echo "Processing: $file"
done

# For loop with C-style syntax
for ((i=0; i<10; i++)); do
    echo "Iteration $i"
done

# While loop
while read -r line; do
    echo "$line"
done < input.txt

# Case statement
case "$extension" in
    .txt) echo "Text file" ;;
    .md)  echo "Markdown" ;;
    .py)  echo "Python" ;;
    *)    echo "Unknown" ;;
esac
```

## How It Works

When Bash executes a script, it follows this sequence:

1. **Startup**: Reads initialization files (`/etc/profile`, `~/.bashrc`, `~/.bash_profile`) to set environment.
2. **Parsing**: Reads input, expands variables (`$VAR`), command substitution (`` `cmd` `` or `$(cmd)`), arithmetic (`$((expr))`), and globs (`*.txt`).
3. **Quote Removal**: Removes quotes that prevented expansion.
4. **Redirection**: Sets up file descriptors for stdin, stdout, stderr as specified.
5. **Execution**: Looks up commands (built-ins, functions, aliases,PATH executables) and runs them.
6. **Wait/Resume**: For interactive shells, waits for next command; for scripts, exits with status.

Understanding this phases helps debugging: variable expansion happens before execution, so `echo "$filename"` prints the value, not the literal name.

## Practical Applications

**System Administration**: Bash scripts automate user management, log rotation, backups, service monitoring, and deployment pipelines. Most DevOps tooling (Ansible modules, Docker entrypoints) ultimately execute Bash under the hood.

**CI/CD Pipelines**: Build scripts, test runners, and deployment automations are commonly written in Bash. GitHub Actions, GitLab CI, and Jenkins all use Bash as a primary scripting language for pipeline steps.

**Data Processing**: While Python excels at complex data transformation, Bash handles one-liners and pipeline-based processing elegantly. `grep`, `sed`, `awk`, and `sort` form a powerful text processing toolkit.

```bash
# Find largest files, sorted
du -sh */ | sort -rh | head -10

# Extract and count unique IP addresses from logs
grep "GET /api" access.log | cut -d' ' -f1 | sort | uniq -c | sort -rn

# Monitor resource usage
watch -n 1 'df -h; echo "---"; free -h'
```

## Examples

**File Processing Pipeline**:
```bash
#!/bin/bash
# Process CSV files: extract columns, filter rows, generate summary

input_dir="./data"
output_file="summary.csv"

echo "timestamp,user_id,action,count" > "$output_file"

for csv in "$input_dir"/*.csv; do
    # Extract relevant columns, filter rows where count > 0
    tail -n +2 "$csv" | awk -F',' '$4 > 0 {print $1","$2","$3","$4}' >> "$output_file"
done

echo "Processed $(ls "$input_dir"/*.csv | wc -l) files into $output_file"
```

**Interactive Menu**:
```bash
echo "Select an option:"
select opt in "Deploy" "Rollback" "Scale" "Exit"; do
    case $opt in
        Deploy)  deploy_app; break ;;
        Rollback) rollback_app; break ;;
        Scale)   scale_app; break ;;
        Exit)    echo "Goodbye"; break ;;
    esac
done
```

## Related Concepts

- [[Shell Scripting]] — General scripting in Unix shells
- [[Terminal]] — Terminal emulators and CLI basics
- [[Zsh]] — Another popular Unix shell with enhanced features
- [[Process Management]] — Running and managing processes in Bash
- [[Environment Variables]] — Managing the process environment

## Further Reading

- Bash Reference Manual: https://www.gnu.org/software/bash/manual/
- "Learning the Bash Shell" by Cameron Newham — Comprehensive introduction
- "Advanced Bash-Scripting Guide" — Deep dive into Bash scripting

## Personal Notes

Bash is a force multiplier. What takes 10 clicks in a GUI can be one line in Bash. I've found that investing time in learning `awk` and `sed` pays off enormously for log analysis and data extraction. The cryptic syntax is actually quite consistent once you internalize that everything expands before execution—that's why quoting matters so much.
