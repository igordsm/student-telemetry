function request_token() {
    if (localStorage.getItem("token") === null) {
        let token = prompt("Entre com seu token");
        localStorage.setItem("token", token);
        return token;
    } else {
        return localStorage.getItem("token");
    }
}

function get_activity_name(item) {
    let item_classes = Array.from(item.classList);
    // Finds a class not admonition or question
    let item_name = item_classes.find(cl => cl != "admonition" && cl != "question");
    if (item_name === undefined) {
        item_name = item.querySelector(".admonition-title").innerText;
    }
    console.log(item_name);
    return item_name;
}

function response_confirmation(evt) {
    let data = evt.data; 
    if (data["message"] == "Invalid token") {
        alert("Token inválido.");
        localStorage.removeItem("token");
        request_token();
    } else {
        let activity_id = data["activity_id"];
        let submitted_answer = data["content"];
        let correct_answer = data["correct_answer"];

        let submitted_item = document.querySelector("#" + activity_id + "-" + submitted_answer);
        if (submitted_item) submitted_item.style.background = "red";

        let correct_item = document.querySelector("#" + activity_id + "-" + correct_answer);
        if (correct_item) correct_item.style.background = "green";

    }

}

document.addEventListener('DOMContentLoaded', (ev) => {
    window.addEventListener("message", response_confirmation);

    let iframe_requester = document.createElement('iframe');
    iframe_requester.style.display = 'none';
    iframe_requester.src = window.submissions_url + "/js/client_iframe.html";
    document.body.appendChild(iframe_requester);

    let questions = document.body.querySelectorAll('.admonition.question');
    
    questions.forEach((item) => {
        let list = Array.from(item.querySelectorAll('ul')).pop()
        if (list !== undefined) {
            let correct_block = item.querySelector('.admonition.done');
            if (correct_block) {
                correct_block.style.display = "none";
            }


            let activity_name = get_activity_name(item);
            let form = document.createElement('div');
            
            let options = list.querySelectorAll('li');

            let item_position = 0;
            options.forEach((opt) => {
                let item_letter = 'ABCDE'.charAt(parseInt(item_position));
                let opt_radio = document.createElement('input');
                opt_radio.setAttribute('type', 'radio');
                opt_radio.setAttribute('name', 'content');
                opt_radio.setAttribute('value', item_letter);

                let opt_label = document.createElement('label');
                opt_label.id = activity_name + "-" + item_letter
                opt_label.appendChild(opt_radio);
                opt_label.appendChild(document.createTextNode(opt.innerText));

                form.appendChild(opt_label);
                form.appendChild(document.createElement('br'));
                item_position++;
            });

            let submit_button = document.createElement('button');
            submit_button.innerText = 'Enviar';
            submit_button.addEventListener("click", () => {
                let selected = "";
                form.querySelectorAll("input[type=radio]").forEach((el) => {
                    if (el.checked) selected = el.value;
                });
                if (selected != "") {
                    let token = request_token();
                    iframe_requester.contentWindow.postMessage(
                        {"course_id": window.course_id, "activity_id": activity_name, "content": selected, "token": token}, "*");
                    
                        submit_button.disabled = true;
                        if (correct_block) {
                            correct_block.style.display = "block";
                            console.log(correct_block.style.display);
                        }
                }
            });

            form.appendChild(submit_button);

            list.remove();
            item.appendChild(form);
        }
        
    })
});