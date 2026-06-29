document.getElementById('searchForm').addEventListener('submit', async function(event) {
    event.preventDefault(); 
    const query = document.getElementById('query').value.trim();
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = 'Loading...';

    if (!query) {
        resultsContainer.innerHTML = '<p class="error">Please enter a search query.</p>';
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/search?q=${encodeURIComponent(query)}`);
        let data = null;
        if (response.ok) {
            data = await response.json();
        }

        const isDataInvalid =
            !data ||
            Object.keys(data).length === 0 ||
            data.error ||
            (Array.isArray(data) && data.length === 0);

        let prompt;

        if (isDataInvalid) {
            prompt = `The user asked: "${query}". Please explain the what is it about, and explain the legal context,Indian laws involved if any, and offer helpful advice or information.`;
        } else {
            const formatted = JSON.stringify(data, null, 2);
            const prefix = "Please analyze the following legal information and write the key points, laws, and advice and also provide some links\n\n";
            const suffix = "\n\nAvoid special characters in the output also start it directly with the name itself.";
            prompt = `${prefix}${formatted}${suffix}`;
        }

        const geminiResponse = await fetch('http://127.0.0.1:5001/ask_gemini', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt })
        });

        if (!geminiResponse.ok) {
            const errorText = await geminiResponse.text();
            throw new Error(`Gemini API failed: ${errorText}`);
        }

        const geminiText = await geminiResponse.text();
        resultsContainer.innerHTML = `<pre>${geminiText}</pre>`;

    } catch (error) {
        console.error('Search failed:', error);
        resultsContainer.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
});
