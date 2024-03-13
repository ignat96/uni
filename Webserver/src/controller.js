class View {
    constructor() {
        // init fields
        this.folder_items = {}
        this.clicked_item = {}

        // init HTMLElement references
        this.table = document.querySelector("#main_table>tbody")
        this.folders_list = document.querySelector("#folders_list")
        this.new_button = document.getElementById("new_btn")
        this.close_button = document.getElementById("close_btn")
        this.add_button = document.getElementById("add_btn")
        this.qsave_button = document.getElementById("quicksave_btn")
        this.back_button = document.getElementById("back_btn")

    }

    add_row(){
        let cell = document.createElement("tr")
        for (let i = 0; i < 6; i++) {
            let td = document.createElement("td")
            td.innerText = "0"
            td.setAttribute("contenteditable", true)
            cell.appendChild(td)
        }
        this.table.appendChild(cell)
    }

    render_list(data){
        this.folder_items = data
        this.folders_list.innerHTML = ""
        for (let c of Array.from(data)) {
            let li = document.createElement('li')
            li.innerText = c['name']
            this.folders_list.appendChild(li)
        }
    }

    print_table(data) {
        if (Object.keys(data).length > 0){
            this.table.innerHTML = ""
            let arr = JSON.parse(data)
            arr.forEach(n => {
                let cell = document.createElement("tr")
                for (const nKey in n) {
                    let td = document.createElement("td")
                    td.innerText = n[nKey]
                    td.setAttribute("contenteditable", true)
                    cell.appendChild(td)
                }
                this.table.appendChild(cell)
            })
        }
    }

    clear_table(){
        this.table.innerHTML = ""
    }


    // Event binders
    bind_add_click(handler) {
        this.add_button.addEventListener("mousedown", (event) => {
            handler(event)
        }, false)
    }

    bind_folder_click(handler){
        this.folders_list.addEventListener('dblclick', (event) => {
            const target = event.target
            if (target.tagName === "LI") {
                this.clicked_item = target
                let item = this.folder_items.find((value, index) => target.innerText === value['name'])
                handler(item['name'])
            }
        }, false)
    }

    bind_close_click(handler){
        this.close_button.addEventListener('mousedown', (event) => {
            event.preventDefault()
            handler(event)
        },false)
    }

    bind_save_click(handler){
        this.qsave_button.addEventListener('mousedown', (event) => {
            event.preventDefault()
            let _table = document.querySelector("#main_table")
            
            handler(_table, this.clicked_item.innerText)
        }, false)
    }

    bind_back_click(handler){
        this.back_button.addEventListener('mousedown', (event) => {
            event.preventDefault()
            handler()
        },false)
    }
}

class Controller {
    constructor(model, view) {
        this.model = model
        this.view = view

        // Bind events & handlers
        this.view.bind_add_click(() => this.view.add_row())
        this.view.bind_close_click(this.handle_close_file)
        this.view.bind_folder_click(this.handle_open_folder)
        this.view.bind_save_click(this.handle_save_file)
        // this.view.bind_back_click(this.handle_back_click)

        // init explorer panel
        fetch('/file_api/list')
        .then(data => data.json())
        .then(data => this.view.render_list(data))
    }


    // Event handlers
    handle_open_folder = (value) => {
        fetch(`/file_api/get/${value}`)
        .then(data => data.json())
        .then(data => this.view.print_table(data))
    }


    handle_close_file = () => {
        this.view.clear_table()
    }

    handle_save_file = (el, name) => {
        let data = []
        for (var i = 1; i < el.rows.length; i++) {
            let table_row = el.rows[i];
            let p = {
                "name": table_row.cells[0].innerText,
                "age": table_row.cells[1].innerText,
                "gender": table_row.cells[2].innerText,
                "group": table_row.cells[3].innerText,
                "course": table_row.cells[4].innerText,
                "rate": table_row.cells[5].innerText,
            }
            data.push(p);
        }

        let request = {
            file_name: name,
            data: data
        }

        fetch(('/file_api/upload'), {
            method: 'POST', 
            body: JSON.stringify(request),
            headers:{
                'Content-Type': 'application/json; charset=UTF-8'
            }
        })
    }



    // Other funcs
    new_alert(code, desc){
        alert(`Error ${code}: ${desc}`)
    }
}

class Model {
    get_file_list(){
        
    }
}
window.addEventListener('DOMContentLoaded', () => {
    app = new Controller(new Model(), new View())
})
// var app
// window.addEventListener('pywebviewready', () => {
//     app = new Controller(pywebview.api, new View())
// }, true)