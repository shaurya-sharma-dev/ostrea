// Database object
const db = makeStandardDatabaseObject();

// Button div with bottom padding
const buttonDiv = document.createElement("div");
buttonDiv.classList.add("pb-4")

// Div for actual page content
const subContainerDiv = document.createElement("div");

// Get dashboard div and add the new div elements to it.
const dashboardDiv = document.getElementById("dashboard");
dashboardDiv.appendChild(buttonDiv)
dashboardDiv.appendChild(subContainerDiv);

// pageState object
var pageState = null;

async function showAddOysterPrompt(){
    var token = prompt("Enter the token of the oyster here.\n\nWarning: You can only have one oyster at a time, meaning if you have an oyster right now, it will be overridden by this new oyster (if it exists)."); 
    if (token !== null) {
        let oysterData = await fetchAPI("/api/oyster/get?token=" + token); 
        if (oysterData !== 404){
            db.put("oyster", 1, {"token": token}); 
            window.location.reload();
        } else {
            alert("Oyster not found.")
        }
    }
}

async function updatePage(){
    if (pageState === null){
        console.error("No page state selected.")
        return;
    }
    
    let stateId = pageState.state;

    if (stateId === "localCreation"){
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

    } else if (stateId === "studentTracker"){
        let oysters = await db.getAllOfType("oyster");
        let btn = document.getElementById("state-toggle");
        btn.innerText = "Switch to Lessons";
        subContainerDiv.innerHTML = "";
        if (oysters.length == 0){
            subContainerDiv.insertAdjacentHTML("beforeend", "<p>You don't have an oyster added yet to your dashboard. Try adding one to track its growth!</p>")
        }
        else {
            let canvas = document.createElement("canvas");
            let ctx = canvas.getContext("2d");
            subContainerDiv.appendChild(canvas);
            loadOysterGraph(ctx, oysters[0].token);
        }

    } else if (stateId === "studentLessonLanding"){
        let units = await fetchAPI("/api/lessons/get-all-units");
        let btn = document.getElementById("state-toggle");
        btn.innerText = "Switch to Tracker";
        subContainerDiv.innerHTML = "";
        if (units.length === 0){
            subContainerDiv.insertAdjacentHTML("beforeend", "<p class='pt-4'>Lessons coming soon!</p>")
        } else {
            for (var i = 0; i < units.length; i ++){
                let desc = units[i].description || "No description provided.";
                let lessonCount = (await fetchAPI(`/api/lessons/get-lessons-in-unit?unit_id=${units[i].id}`)).length;
                subContainerDiv.insertAdjacentHTML("beforeend", `<div class='py-2 px-2 rounded-sm border-solid border-gray-500 border'>
                    <h2 class='text-2xl font-bold py-2'>${units[i].name}</h2>
                    <p class='py-2'>Lesson Count: ${lessonCount}</p>
                    <p class='py-2'>${desc}</p>
                    </div>
                    <br>`
                )
            }
        }

    } else if (stateId === "teacherLanding"){
        subContainerDiv.innerHTML = "";
        subContainerDiv.insertAdjacentHTML("beforebegin", "<p>You are a teacher.</p>");

    } else {
        console.error("Invalid page state ID:", stateId);
    }
}

async function toggleStudentState() {
    pageState = {
        "state": pageState.state === "studentLessonLanding" ? "studentTracker" : "studentLessonLanding",
    };

    updatePage();
}

async function main() {
    const user = await getUserObject(db);
    if (user === null){
        pageState = {
            "state": "localCreation",
        }

    } else{
        buttonDiv.insertAdjacentHTML("afterbegin", `
            <button class="rounded-md bg-red-600 hover:bg-red-700 cursor-pointer py-2 px-2" onclick='if (confirm("Are you sure you want to wipe all of your local Ostrea data? If you proceed with this, the data CANNOT BE RECOVERED.")) {db.deleteDB(); window.location.reload();}'>Wipe Data</button>
        `)
        if (user.role === "student"){
            buttonDiv.insertAdjacentHTML("afterbegin", `
                <button class="rounded-md bg-blue-500 hover:bg-blue-700 cursor-pointer py-2 px-2" onclick='showAddOysterPrompt();'>Add Oyster</button>
                <button class="rounded-md bg-blue-500 hover:bg-blue-700 cursor-pointer py-2 px-2" onclick='toggleStudentState();' id='state-toggle'></button>
            `)

            pageState = {
                "state": "studentTracker"
            };
        } else if (user.role == "teacher"){
            pageState = {
                "state": "teacherLanding"
            };
        }
    }

    updatePage();
}

db.connect().then(()=>{
    main();
});