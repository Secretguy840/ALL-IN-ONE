// Requires dialogflow package: npm install dialogflow
const dialogflow = require('@google-cloud/dialogflow');
const uuid = require('uuid');

async function detectIntent(projectId, sessionId, query, languageCode) {
    const sessionClient = new dialogflow.SessionsClient();
    const sessionPath = sessionClient.projectAgentSessionPath(projectId, sessionId);
    
    const request = {
        session: sessionPath,
        queryInput: {
            text: {
                text: query,
                languageCode: languageCode,
            },
        },
    };
    
    const responses = await sessionClient.detectIntent(request);
    const result = responses[0].queryResult;
    
    console.log(`Query: ${result.queryText}`);
    console.log(`Response: ${result.fulfillmentText}`);
    
    if (result.intent) {
        console.log(`Intent: ${result.intent.displayName}`);
    } else {
        console.log('No intent matched.');
    }
    
    return result;
}

// Example usage
const projectId = 'your-project-id';
const sessionId = uuid.v4();
detectIntent(projectId, sessionId, 'Hello', 'en-US');