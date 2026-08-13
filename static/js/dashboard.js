const dashboardDiv = document.getElementById("dashboard");
const db = makeStandardDatabaseObject();
const subContainerDiv = document.createElement("div");
dashboardDiv.appendChild(subContainerDiv);

async function showAddOysterPrompt(){
    var token = prompt("Enter the token of the oyster here.\n\nWarning: You can only have one oyster at a time, meaning if you have an oyster right now, it will be overridden by this new oyster (if it exists)."); 
    if (token !== null) {
        let oysterData = await fetchAPI("/api/oyster/get?token=" + token); 
        if (oysterData !== 404){
            db.put("oyster", 1, {"token": token}); window.location.reload();
        } else {
            alert("Oyster not found.")
        }
    }
}

async function toggleState() {
    subContainerDiv.innerHTML = "";

    let btn = document.getElementById("state-toggle");
    btn.innerText = btn.innerText === "Switch to Lessons" ? "Switch to Tracker" : "Switch to Lessons";

    let is_tracker = btn.innerText.includes("Lessons");

    if (is_tracker){
        let oysters = await db.getAllOfType("oyster");
        if (oysters.length == 0){
            subContainerDiv.insertAdjacentHTML("beforeend", "<p class='pt-4'>You don't have an oyster added yet to your dashboard. Try adding one to track its growth!</p>")
        }
        else {
            let canvas = document.createElement("canvas");
            let ctx = canvas.getContext("2d");
            subContainerDiv.appendChild(canvas);
            loadOysterGraph(ctx, oysters[0].token);
        }
    } else {
        subContainerDiv.insertAdjacentHTML("beforeend", "<p class='pt-4'>Lessons coming soon.</p>")
    }
}

async function main() {
    const user = await getUserObject(db);
    if (user === null){
        dashboardDiv.insertAdjacentHTML("beforebegin", `<form id="profile-create-form">
    <h2 class="text-3xl font-bold py-4">Create Local Profile</h2>
    <p>This information will be stored on your device, and it is required in order to properly use Ostrea.</p>
    <p>Are you a teacher or student?</p>
    <br>
    <div class="grid grid-cols-2 gap-4 text-white">
        <button class="rounded-full bg-blue-500 hover:bg-blue-700 cursor-pointer py-2" onclick='db.put("user", 1, {"joined": new Date(), "role": "student"});'>Student</button>
        <button class="rounded-full bg-blue-500 hover:bg-blue-700 cursor-pointer py-2" onclick='db.put("user", 1, {"joined": new Date(), "role": "teacher"});'>Teacher</button>
    </div>
</form>`);
        
    } else{
        dashboardDiv.insertAdjacentHTML("beforebegin", `
            <button class="rounded-full bg-red-600 hover:bg-red-700 cursor-pointer py-2 px-2" onclick='if (confirm("Are you sure you want to wipe all of your local Ostrea data? If you proceed with this, the data CANNOT BE RECOVERED.")) {db.deleteDB(); window.location.reload();}'>Wipe Data</button>
        `)
        if (user.role === "student"){
            dashboardDiv.insertAdjacentHTML("beforebegin", `
                <button class="rounded-full bg-blue-500 hover:bg-blue-700 cursor-pointer py-2 px-2" onclick='showAddOysterPrompt();'>Add Oyster</button>
                <button class="rounded-full bg-blue-500 hover:bg-blue-700 cursor-pointer py-2 px-2" onclick='toggleState();' id='state-toggle'>Switch to Tracker</button>
            `)
            toggleState();
        } else if (user.role == "teacher"){
            subContainerDiv.insertAdjacentHTML("beforebegin", "<p class='pt-4'>You are a teacher.</p>")
        }
    }
}

db.connect().then(()=>{main()});