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

function loadOysterGraph(ctx, token, attribute, yAxisLabel){
    fetchAPI("/api/oyster/get?token=" + token).then(oysterData => {
        var data = [[oysterData.name]];
        oysterData.oysterlog_set.forEach(element => {
            data[0].push([element.date, parseFloat(element[attribute])]);
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

        new Chart(ctx, {
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
                            text: yAxisLabel
                        },
                    }
                }
            }
        });
    });
}

function submitCheck(){
    let lesson = pageState.lessonObject;
    let totalQuestions = lesson.question_set.length;
    let correctQuestions = 0;
    let allAnswered = true;
    for (var i = 0; i < totalQuestions; i++){
        let selectedAnswer = document.querySelector(`input[name="question${i}"]:checked`);
        if (selectedAnswer !== null){
            if (selectedAnswer.value == lesson.question_set[i].correct_choice){
                correctQuestions ++;
            }
        } else {
            allAnswered = false;
            break;
        }
    }

    if (allAnswered){
        db.put("lessons", pageState.lessonId, {"correctQuestions": correctQuestions, "totalQuestions": totalQuestions});
        window.location.reload();
    } else {
        alert("You have not answered all questions in this lesson.")
    }
}

async function startCheck(){
    let prevScore = await db.getSafe("lessons", pageState.lessonId);
    if (prevScore !== null && prevScore.correctQuestions === prevScore.totalQuestions){
        if (!confirm("Are you sure you want to start this lesson? You have already attained a score of 100%.\n\nPress OK to continue or Cancel to exit.")){
            return;
        }
    }
    let lesson = pageState.lessonObject;
    let container = document.getElementById("check-container");
    container.innerHTML = "";
    let totalQuestions = lesson.question_set.length;
    
    for (var i = 0; i < totalQuestions; i++){
        let answers = [
            lesson.question_set[i].correct_choice,
            lesson.question_set[i].incorrect_choice_1,
            lesson.question_set[i].incorrect_choice_2,
            lesson.question_set[i].incorrect_choice_3,
        ];

        // Shuffle answers list.
        for (var j = answers.length - 1; j > 0; j--) {
            const k = Math.floor(Math.random() * (j + 1));
            [answers[j], answers[k]] = [answers[k], answers[j]];
        }

        for (var j = 0; j < answers.length; j++){
            answer = answers[j];
            answers[j] = `
                <input type="radio" id="question${i}choice${j}" name="question${i}" value="${answer}" />
                <label for="question${i}choice${j}">${answer}</label>
            `;
        }

        container.insertAdjacentHTML("beforeend", `
            <p class="font-bold py-2">${lesson.question_set[i].text}</p>
            ${answers.join("<br>")}
        `)
    }

    container.insertAdjacentHTML("beforeend", `
        <br>
        <br>
        <button class="bg-blue-500 hover:bg-blue-700 cursor-pointer rounded-md py-2 px-2" onclick="submitCheck();">Submit Work</button>
    `)
}

const ARTICLE_KEYWORDS = {
    "INTERACTIVE:OYSTER_ANATOMY_FLASHCARDS": `<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vQWy9V23B4DXxJmpX5OCnaPfYOWz4hkJ49jFsOb5gq1sXnFQWnCO4cVt0Qhk1NBhu8xjMPN2tzG3IK1/pubembed?start=false&loop=false&delayms=3000" frameborder="0" width="480" height="299" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>`,
    "INTERACTIVE:OYSTER_ANATOMY_CHATBOT": `<iframe src="/games/anatomy-chatbot/" title="Oyster Anatomy Chatbot" class="w-full max-w-5xl min-h-[85vh]"></iframe>`,
    "GAME:LIFECYCLE_TIMELINE": `<iframe src="/games/lifecycle-timeline/" title="Oyster Lifecycle Timeline" class="w-full max-w-5xl min-h-[85vh]"></iframe>`,
    "GAME:HABITAT_SURVIVAL_YES_NO": `<iframe src="/games/habitat-survival/" title="Oyster Lifecycle Timeline" class="w-full max-w-5xl min-h-[85vh]"></iframe>`,
}

async function buildDOM(){
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
            subContainerDiv.insertAdjacentHTML("beforeend", "<p>Track your oyster with the graphs below! All dates are formatted as YYYY-MM-DD.</p>");
            subContainerDiv.appendChild(canvas);
            loadOysterGraph(ctx, oysters[0].token, "salinity", "Salinity (PPT)");
        }

    } else if (stateId === "studentLessonLanding"){
        let btn = document.getElementById("state-toggle");
        btn.innerText = "Switch to Tracker";
        subContainerDiv.innerHTML = "";

        if (pageState.display && pageState.display !== null){
            let lessons = await fetchAPI(`/api/lessons/get-lessons-in-unit?unit_id=${pageState.unitId}`);

            if (pageState.display == "unit"){
                // Show all lessons in a unit.
                let unit = await fetchAPI(`/api/lessons/get-unit?unit_id=${pageState.unitId}`);
                subContainerDiv.insertAdjacentHTML("beforeend", `
                    <h2 class='text-3xl font-bold py-2'>${unit.name}</h2>
                    <p>${unit.description || "No description provided."}</p>
                    <button class="rounded-md bg-blue-500 hover:bg-blue-700 cursor-pointer py-2 px-2" onclick='pageState = {"state": "studentLessonLanding"}; updatePage();'>Back to All Units</button>
                `)
                for (var i = 0; i < lessons.length; i ++){
                    subContainerDiv.insertAdjacentHTML("beforeend", `
                        <h3 class='text-2xl font-bold py-2'>${lessons[i].name}</h3>
                        <button class="rounded-md bg-blue-500 hover:bg-blue-700 cursor-pointer py-2 px-2" onclick='pageState = {"state": "studentLessonLanding", "display": "lesson", "unitId": "${unit.id}", "lessonId": ${lessons[i].id}}; updatePage();'>Start Lesson</button>
                    `)
                }

            } else if (pageState.display == "lesson"){
                // Show one lesson.
                let lesson = lessons.filter(l => l.id === pageState.lessonId)[0];
                pageState.lessonObject = lesson;
                let prevScore = await db.getSafe("lessons", pageState.lessonId);
                prevScore = prevScore === null ? "---" : `${(prevScore.correctQuestions / prevScore.totalQuestions) * 100}%`;
                let parsed = parseMarkdown(lesson.article);
                let finalArticle = Object.entries(ARTICLE_KEYWORDS).reduce((str, [key, value]) => {
                    return str.replaceAll(key, value);
                }, parsed);
                subContainerDiv.insertAdjacentHTML("beforeend", `
                    <h1 class='text-4xl font-bold py-2'>${lesson.name}</h1>
                    <button class="rounded-md bg-blue-500 hover:bg-blue-700 cursor-pointer py-2 px-2" onclick='pageState = {"state": "studentLessonLanding", "display": "unit", "unitId": "${pageState.unitId}"}; updatePage();'>Back to Unit</button>
                    ${finalArticle} 
                    ${lesson.question_set.length === 0 ? 
                        '<p class="py-4">You have finished this lesson. Feel free to move on to the next one once you\'re ready!</p>': 
                        `<h2 class="text-3xl font-bold py-2">Show What You Know!</h2>
                        <p>Previous Score: ${prevScore}</p>
                        <div id="check-container">
                            <button 
                                class="rounded-md bg-blue-500 hover:bg-blue-700 cursor-pointer py-2 px-2" 
                                onclick=\'startCheck()\'
                            >
                            Start Check for Understanding
                            </button>
                        </div>`
                    }
                `)
            }

        }

        else {
            let units = await fetchAPI("/api/lessons/get-all-units");
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
                        <button class="rounded-md bg-blue-500 hover:bg-blue-700 cursor-pointer py-2 px-2" onclick='pageState = {"state": "studentLessonLanding", "display": "unit", "unitId": "${units[i].id}"}; updatePage();'>Open Unit</button>
                        </div>
                        <br>`
                    )
                }
            }
        }

    } else if (stateId === "teacherLanding"){
        subContainerDiv.innerHTML = "";
        subContainerDiv.insertAdjacentHTML("beforebegin", `<h2 class="text-3xl font-bold py-2">Welcome, teacher!</h2>
        <p>How will you use Ostrea today?</p>
        <div class="grid grid-cols-3 gap-4 text-white py-4">
            <button class="rounded-full bg-blue-500 hover:bg-blue-700 cursor-pointer py-2" onclick='console.log("add student");'>Add Student</button>
            <button class="rounded-full bg-blue-500 hover:bg-blue-700 cursor-pointer py-2" onclick='console.log("request sync");'>Request Sync</button>
            <button class="rounded-full bg-blue-500 hover:bg-blue-700 cursor-pointer py-2" onclick='console.log("view data");'>View Student Data</button>
        </div>`);

    } else {
        console.error("Invalid page state ID:", stateId);
    }
}

function updatePage(){
    pageState.page = pageState.state;
    delete pageState.state;
    let href = `/dashboard?`;
    for (const [key, value] of Object.entries(pageState)) {
        href += `${key}=${value}&`;
    }
    window.location.href = href
}

async function toggleStudentState() {
    pageState = {
        "state": pageState.state === "studentLessonLanding" ? "studentTracker" : "studentLessonLanding",
    };

    updatePage();
}

db.connect().then(async () => {
    const user = await getUserObject(db);
    const urlParams = new URLSearchParams(window.location.search);
    let pageId = urlParams.get("page");

    if (user === null){
        if (pageId === null){
        // If no user has been created, ignore query params and go to local creation.
        window.location.replace("/dashboard?page=localCreation");
        }
        pageState = {"state": "localCreation"}

    } else{
        if (window.location.search === ""){
            if (user.role === "student"){
                window.location.replace("/dashboard?page=studentTracker");
            } else if (user.role == "teacher"){
                window.location.replace("/dashboard?page=teacherLanding");
            }
        } else {
            if (pageId === "localCreation"){
                window.location.replace("/dashboard");
            }
            if (user.role === "student" && (pageId.includes("teacher") || pageId === null)){
                window.location.replace("/dashboard?page=studentTracker");
            } else if (user.role === "teacher" && (pageId.includes("student") || pageId === null)){
                window.location.replace("/dashboard?page=teacherLanding");
            } else {
                const VALID_PAGES = ["studentTracker", "studentLessonLanding", "teacherLanding"];
                if (VALID_PAGES.includes(pageId)){
                    buttonDiv.insertAdjacentHTML("afterbegin", `
                        <button class="rounded-md bg-red-600 hover:bg-red-700 cursor-pointer py-2 px-2" onclick='if (confirm("Are you sure you want to wipe all of your local Ostrea data? If you proceed with this, the data CANNOT BE RECOVERED.")) {db.deleteDB(); localStorage.clear(); window.location.reload();}'>Wipe Data</button>
                    `)
                    if (user.role === "student"){
                        buttonDiv.insertAdjacentHTML("afterbegin", `
                            <button class="rounded-md bg-blue-500 hover:bg-blue-700 cursor-pointer py-2 px-2" onclick='showAddOysterPrompt();'>Add Oyster</button>
                            <button class="rounded-md bg-blue-500 hover:bg-blue-700 cursor-pointer py-2 px-2" onclick='toggleStudentState();' id='state-toggle'></button>
                        `)
                    }

                    pageState = {
                        "state": pageId
                    };
                    urlParams.forEach((value, key) => {
                        if (key === "page"){
                            return;
                        } else {
                            if (key == "lessonId"){
                                pageState[key] = Number(value);
                                if (pageState[key] === NaN){
                                    window.location.replace("/dashboard");
                                }
                                return;
                            }
                            pageState[key] = value;
                        }
                    });
                } else {
                    window.location.replace("/dashboard");
                }
            }
        }
    }

    buildDOM();
});