document.addEventListener("DOMContentLoaded", (event) => {
    window.addEventListener("message", (event) => {
        let course_id = event.data["course_id"];
        let activity_id = event.data["activity_id"];
        
        let formData = new FormData();
        formData.append("token", event.data["token"]);
        formData.append("content", event.data["content"]);
        formData.append("type", "multiple_choice");
        
        let return_window = window.parent;

        fetch("/courses/" + course_id + "/activities/" + activity_id, {
            "method": "POST",
            "body": formData
        }).then((response) => {
            if (response.status == 200) return response.json()
            else if (response.status == 401) return {"message": "Invalid token"};
            else return {};
        }).then((data) => {
            return_window.postMessage(data, "*");
        });
    });
});