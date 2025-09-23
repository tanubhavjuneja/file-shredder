flowchart TD
  A[User selects target(s)] --> B{Target is file or directory?}
  B --> |file| C[Encrypt file (ephemeral key)]
  B --> |dir| D[Iterate files in dir -> each file -> Encrypt]
  C --> E[Overwrite file (passes, chunk size)]
  D --> E
  E --> F[Random rename & overwrite (optional)]
  F --> G[Delete file]
  G --> H{Wipe free space?}
  H --> |Yes| I[Create filler file -> write chunks -> delete filler]
  H --> |No| J[Done]
  I --> J
  J --> K[Log results & notify user]
