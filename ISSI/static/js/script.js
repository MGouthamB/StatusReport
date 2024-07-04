let taskCounter = 2;
    const listElement = document.getElementById("tasksList");
    
    function addTaskRow() {
        const childListElement = document.createElement("li");
        childListElement.id = `task${taskCounter}`;
        childListElement.name = `task${taskCounter}`;
        childListElement.innerHTML = `<label for="project${taskCounter}">Project</label>
            <select name="project${taskCounter}" id="project${taskCounter}">
                {% for key, value in projects.items %}
                <option value="{{ key }}">{{ value }}</option>
                {% endfor %}
            </select>
            <label for="taskName${taskCounter}">Task Name</label>
            <input type="text" id="taskName${taskCounter}" name="taskName${taskCounter}" placeholder="Task Name">

            <label for="taskDescription${taskCounter}">Task Description</label>
            <input type="text" id="taskDescription${taskCounter}" name="taskDescription${taskCounter}" placeholder="Task Description">
    
            <label for="status${taskCounter}">Status of the Task</label>
            <select name="status${taskCounter}" id="status${taskCounter}">
                <option value="completed">Completed</option>
                <option value="progress">In progress</option>
                <option value="start">YET-TO-START</option>
            </select>
            <button class="close-button" aria-label="Close alert" type="button" data-close>
                <span aria-hidden="true">&times;</span>
              </button>`;
        listElement.appendChild(childListElement);
        taskCounter++;
    }

    function onSubmit(event) {
        event.preventDefault();
        const formData = new FormData();
        for (let i = 1; i < taskCounter; i++) {
            const tempData = new FormData();
            console.log(document.getElementById(`project${i}`).value);
            console.log(document.getElementById(`project${i}`).value);
            console.log(document.getElementById(`taskDescription${i}`).value)
            console.log(document.getElementById(`status${i}`).value)
            tempData.append("project", document.getElementById(`project${i}`).value);
            tempData.append("taskName", document.getElementById(`taskName${i}`).value);
            tempData.append("taskDescription", document.getElementById(`taskDescription${i}`).value);
            tempData.append("status", document.getElementById(`status${i}`).value);
            console.log(tempData)
            formData.append(`task${i}`, tempData);
        }
        console.log(formData);
        const token = document.getElementById("token").value;
        const headers = {
            "X-CSRFToken": token,
            "Content-Type": "multipart/form"
        };
        
        axios.post("/statusReport/createTask", formData, { headers })
            .then(response => console.log(response))
            .catch(error => console.log(error));
    }