// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

async function fetchAPI(url) {       
    try {
        const response = await fetch(url);
        
        if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;

    } catch (error) {
        // Catch network issues or parsing failures
        console.error("Fetch operation failed:", error.message);
    }
}