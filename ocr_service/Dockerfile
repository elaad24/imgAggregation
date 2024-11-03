# Step 1: Use an official Node image as the base
FROM node:16-alpine

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy package.json and package-lock.json, and install dependencies
COPY package*.json ./
RUN npm install

# Step 4: Copy the rest of the application code
COPY . .

# Step 5: Build the TypeScript code
RUN npm run build

# Step 6: Expose the application port
EXPOSE 3000

# Step 7: Command to run the application
CMD ["node", "dist/index.js"]
