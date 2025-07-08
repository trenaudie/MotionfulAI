# Motion Graphics AI Project

This project aims to automate the creation of Motion Canvas code in Typescript, using AI tools such as Claude Code, Llama, Groq, and others. 
The idea is to ultimately build the Cursor but for Motion-Canvas. 

## Main Project 
The core project will be an agent workflow that:
1. Generate new code using Claude Code.(eg. Cat and human) 
2. Generate the image for it
3. Generate a review of the image, and code. Using multimodal LLM like Llama.
5. Repeat 1 through 3 until satisfying result

## Implementation notes
The tool will use Claude Code (or other chat based SDK) to view the files and edit them. 
We will need to build an asynchronous rendering function for Motion Canvas to feed results into a Multi Modal LLM 

Style and optimization notes: 
Ideally the project would be tailored for maths visualizations and black on white clean assets, for excalidraw-esque explanatory slides, with animations. 

## Project structure
package.json : all available npm commands for this project

