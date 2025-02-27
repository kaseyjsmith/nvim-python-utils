# What it does right now
- Strips tags that from lines that contain '\[x\]'

# What I want it to do
- Strips tags that from lines that contain '\[x\]'
- Change #todo tag to #deferred when '\[>\]'

## How should I do this?
1. Update the yaml config to have tag and function
2. If '\[>\]' in line, replace #todo or add #deferred
