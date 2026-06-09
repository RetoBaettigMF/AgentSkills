# Sabbatical Skill - Requirements 

Build me a skill according to the agent-skill specifications in https://agentskills.io/specification that manages all the know-how and information about my sabbatcal in china.

## Data source

All the data is stored as Markdown-files in 
`/Users/morticiamac/Google Drive/Meine Ablage/Markdowns`

A index of the data named `index.md` inside this folder is the starting point to find all the information. 

Build a function that can be called by a cron-job that updates the `index.md` file by recursively going through all the files in the folder and storing a systematic index about all the files and a respective short summary what can be found in the individual files.

Then also build a simple RAG-System. Use a json file as vector database and store just the vector, the path and the last change date of the corresponding file (don't store the content of the file). Don't split the files for the RAG index, always use the entire file.

Build a function that can be called by a cron-job that updates the RAG index. Just update changed or added files and remove the entries in the Vector DB where the file n longer exists.

Build a "search function" that can be called by an agent with a question. Then find the corresponding files using the index.md and the rag system. Then return the content of these files together with the full path names of the files as Sources.

Build a function that can be called by an agent for adding information to the know-How Database. The funciton should work as follows:
- Search for similar information in files by using the "search function"
- If you find a matching file, return a "diff" what you would change
- If you don't find a matching file, return a "diff" for a proposed new file
- The calling agent then will decide whether or not to execute the diffs

Use openrouter for the AI functions, get the Key and the Model names from a .env file.

If you write scripts, write them as 


