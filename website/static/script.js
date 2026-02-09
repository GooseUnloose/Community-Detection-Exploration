
const city_list = [];
let return_response;


function input_sanitiser(input_str){
    //removes all non characters from input_str and returns a list of these separated values

    let parsed_str = input_str.replace(/[^a-zA-Z\s]/g,'');
    let rtn_list = parsed_str.split(" ");
    
    for (let i = 0; i < rtn_list.length;i++){
        if (rtn_list[i] == ''){
            rtn_list.splice(i,1);
            i = -1;
        }
    }

    return rtn_list;
}

function log_city_list (){
    let sanitised_lst = input_sanitiser(document.getElementById('city_input').value);

    for (i = 0; i < sanitised_lst.length;i++){
        if(city_list.indexOf(sanitised_lst[i]) == -1){
            city_list.push(sanitised_lst[i]);
        }
    }

    document.getElementById('community_output').innerHTML = city_list;
};

function create_community_div(JSON_response){
    const keys = Object.keys(JSON_response);

    const house_div = document.createElement('div');
    keys.forEach(element => {
        const com_div = document.createElement('div');
        com_div.className = 'community_div';
        com_div.appendChild(create_response_table(JSON_response,element));

        house_div.appendChild(com_div);
    });

    return house_div;
}


function drag_start_handler(ev){
    ev.preventDefault();
    ev.dataTransfer.setData('Text',ev.target.textContent);
}


function drag_over_handler(ev){
    ev.preventDefault();
}


function drop_handler(ev){
    ev.preventDefault();

    console.log("Drop Complete");

    const drop_data = ev.dataTransfer.getData('Text')
    const row = document.createElement('tr');
    const row_data = document.createElement('td');

    row_data.textContent = drop_data;

    row.appendChild(row_data);

    ev.target.appendChild(row);


}



//Creates a new table for each key of the JSON response
function create_response_table(JSON_response,key){
    const com_table = document.createElement('table')

    com_table.ondrop = 'drop_handler(event)';

    com_table.addEventListener('drop',function (e){
        drop_handler(e);
    })

    com_table.ondragover = 'drag_over_handler(event)';

    const header_row = document.createElement('tr');
    const header = document.createElement('th');
    
    header.textContent = key;
    header_row.appendChild(header);
    com_table.appendChild(header_row);


    JSON_response[key].forEach(element => {
        const row = document.createElement('tr');
        const row_data = document.createElement('td');
        row_data.textContent = element;

        row_data.draggable = 'True';
        
        row_data.addEventListener('dragstart', function (e){
            drag_start_handler(e);
        })

        row_data.addEventListener('dragover' , function (e){
            drag_over_handler(e)
        })

        row.appendChild(row_data);
        com_table.appendChild(row);
    });

    return com_table
}


document.getElementById('city_input').addEventListener('keyup',function (event){
    // if event is the enter key, add current value to the city_array 
    if (event.code === 'Enter'){
        log_city_list();
    }
})


document.getElementById('button').addEventListener('click',function (){
    const request = new XMLHttpRequest();

    request.onload = function() {
        return_response = JSON.parse(request.responseText);

        const div_insert = document.getElementById('test');
        div_insert.innerHTML = '';
        div_insert.appendChild(create_community_div(return_response));
    }

    request.open('GET',`/louvain?cities_list=${city_list}`);
    request.send();
})


