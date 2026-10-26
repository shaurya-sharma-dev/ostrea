// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

async function fetchAPI(url) {       
    try {
        const response = await fetch(url);
        
        if (!response.ok) {
            return response.status;
        }
        
        const data = await response.json();
        return data;

    } catch (error) {
        // Catch network issues or parsing failures
        console.error("Fetch operation failed:", error.message);
    }
}

// IndexedDB helper
class Database {
  constructor(dbName) {
    this.dbName = dbName;
    this.dbPromise = null;
    this.storeName = 'store';
    this.indexName = 'type_idx';
  }

  connect() {
    if (this.dbPromise) return this.dbPromise;

    this.dbPromise = new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, 1);

      request.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          const store = db.createObjectStore(this.storeName, { keyPath: 'id' });
          store.createIndex(this.indexName, 'type', { unique: false });
        }
      };

      request.onsuccess = (e) => resolve(e.target.result);
      request.onerror = (e) => {
        this.dbPromise = null;
        reject(request.error);
      };
    });

    return this.dbPromise;
  }

  async put(type, id, data) {
    const db = await this.connect();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, 'readwrite');
      const store = tx.objectStore(this.storeName);
      const record = { ...data, id: `${type}_${id}`, type: type };
      
      const request = store.put(record);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async get(type, id) {
    const db = await this.connect();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, 'readonly');
      const store = tx.objectStore(this.storeName);
      
      const request = store.get(`${type}_${id}`);
      request.onsuccess = () => resolve(request.result || null);
      request.onerror = () => reject(request.error);
    });
  }

  async getSafe(type, id) {
    try {
        return await db.get(type, id);
    } catch (error) {
        if (error.name === 'NotFoundError') {
            console.warn("Caught Error: The requested object does not exist.");
            return null;
        } else {
            console.error("DB Error:", error);
            throw error;
        }
    }
  }

  async getAllOfType(type) {
    const db = await this.connect();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, 'readonly');
      const store = tx.objectStore(this.storeName);
      const prefix = `${type}_`;
      const range = IDBKeyRange.bound(prefix, prefix + '\uffff');
      
      const request = store.getAll(range);
      request.onsuccess = () => resolve(request.result || null);
      request.onerror = () => reject(request.error);
    });
  }

  async delete(type, id) {
    const db = await this.connect();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, 'readwrite');
      const store = tx.objectStore(this.storeName);

      const request = store.delete(`${type}_${id}`);
      request.onsuccess = () => resolve(true);
      request.onerror = () => reject(request.error);
    });
  }

  deleteDB(){
    // Request the deletion of the database
    const request = indexedDB.deleteDatabase(this.dbName);

    // Successfully deleted
    request.onsuccess = (event) => {
        console.log("Database deleted successfully.");
    };

    // Error occurred during deletion
    request.onerror = (event) => {
        console.error("Error deleting database:", event.target.error);
    };

    // Blocked by open connections in other tabs/windows
    request.onblocked = (event) => {
        console.warn("Deletion blocked. Please close all other tabs using this database.");
    };
  }
}

function makeStandardDatabaseObject(){
    return new Database("OstreaStorage");
}

async function getUserObject(db){
    return await db.getSafe('user', 1);
}

function parseMarkdown(text) {
    // Basic Markdown to HTML parser.
    // Edge cases can break it, but since we control the input, it shouldn't
    // be a major issue.

    let html = text;

    html = html.replace(/^### (.*$)/gim, '<h3 class="text-2xl font-bold py-4">$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2 class="text-3xl font-bold py-4">$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1 class="text-4xl font-bold py-4">$1</h1>');

    html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold">$1</strong>');

    html = html.replace(/^\s*[-\*]\s+(.*$)/gim, '<li>$1</li>');

    html = html.replace(/(<li>.*<\/li>)/gim, '<ul class="list-disc pl-5">$1</ul>');
    html = html.replace(/<\/ul>\s*<ul class="list-disc pl-5">/g, ''); 

    html = html.split('\n').map(line => {
        line = line.trim();
        if (!line) {
            return ''
        }; // Skip empty lines

        if (line.match(/^<(h\d|ul|li)/)){
            return line
        };
        
        return `<p>${line}</p>`;
    }).join('\n');

    return html.trim();
}