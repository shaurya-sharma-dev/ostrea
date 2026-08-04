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

function loadOysterGraph(ctx, token){
    fetchAPI("/api/oyster/get?token=" + token).then(oysterData => {
        var data = [[oysterData.name]];
        oysterData.oysterlog_set.forEach(element => {
            data[0].push([element.date, parseFloat(element.ph_level)]);
        });

        const datasets = data.map((series, index) => {
            return {
                label: `${series[0]}`,
                data: series.slice(1, series.length).map(item => ({
                    x: item[0],
                    y: item[1],
                })),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.2
            };
        });

        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: datasets
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'pH Level'
                        },
                        min: 0,
                        max: 14,
                    }
                }
            }
        });
    });
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

    async function handleDOMRemoval() {
        const user = await getUserObject(db);
        if (user !== null){
            let elements = document.querySelectorAll(".remove-for-non-staff");
            for (var i = 0; i < elements.length; i ++){
                elements[i].remove();
            }
        }
    }
    
    document.addEventListener('DOMContentLoaded', () => {
        handleDOMRemoval();
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
}

function makeStandardDatabaseObject(){
    return new Database("OstreaStorage");
}

async function getUserObject(db){
    try {
        return await db.get('user', 1);
    } catch (error) {
        if (error.name === 'NotFoundError') {
            console.warn("Caught Error: The 'user' object does not exist.");
            return null;
        } else {
            console.error("DB Error:", error);
            throw error;
        }
    }
}