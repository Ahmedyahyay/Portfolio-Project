/**
 * CORS Test Script
 * Run this with Node.js to test CORS configuration
 */

const fetch = require('node-fetch');

async function testCORS() {
    console.log('🚀 Testing CORS Configuration...\n');
    
    const baseURL = 'http://localhost:5000';
    const tests = [
        {
            name: 'BMI Endpoint Test',
            url: `${baseURL}/api/bmi`,
            method: 'POST',
            body: { height: 175, weight: 80 }
        },
        {
            name: 'Register Endpoint Test',
            url: `${baseURL}/api/register`, 
            method: 'POST',
            body: { 
                email: 'test@example.com',
                password: 'password123',
                height: 175,
                weight: 90
            }
        }
    ];
    
    for (const test of tests) {
        try {
            console.log(`📋 ${test.name}:`);
            
            const response = await fetch(test.url, {
                method: test.method,
                headers: {
                    'Content-Type': 'application/json',
                    'Origin': 'http://localhost:3000'
                },
                body: JSON.stringify(test.body)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                console.log(`✅ Success (${response.status}):`, data);
            } else {
                console.log(`⚠️  Error (${response.status}):`, data);
            }
            
        } catch (error) {
            console.log(`❌ Failed:`, error.message);
        }
        
        console.log(''); // Empty line for readability
    }
    
    console.log('🏁 CORS testing complete!');
}

// Run the test
testCORS().catch(console.error);