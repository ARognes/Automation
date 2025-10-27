
# Add homebrew bin directory to PATH
export PATH="/opt/homebrew/bin:$PATH"

# Shorten command prompt
PROMPT='%F{green}%~%f %F{cyan}➜%f '

# Add custom Neovim bin directory to PATH
export PATH="$HOME/nvim/bin:$PATH"

# Ensure vi, vim, and nvim point to Neovim
vi() {
  "$HOME/nvim/bin/nvim" "$@"
}

vim() {
  "$HOME/nvim/bin/nvim" "$@"
}

nvim() {
  "$HOME/nvim/bin/nvim" "$@"
}

splitchunks() {
  python3 /Users/arognes/.python/splitchunks.py "$@"
}



