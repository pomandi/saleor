FROM node:18-alpine
WORKDIR /app

# Install pnpm and dependencies
RUN apk add --no-cache libc6-compat
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies first
RUN pnpm install

# Install slider packages
RUN pnpm add react-slick@0.29.0 @types/react-slick@0.23.13 slick-carousel@1.8.1

# Copy the rest of the application
COPY . .

# Set environment variables
ENV NEXT_PUBLIC_SALEOR_API_URL=http://api:8000/graphql/
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1

# Expose the port the app runs on
EXPOSE 3000

# Start the application in development mode
CMD ["sh", "-c", "pnpm install && pnpm dev --turbo"]
