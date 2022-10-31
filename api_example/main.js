



let noplanuserUrl = 'http://127.0.0.1:8000/api/company/1/noplan'
let paiduserUrl = 'http://127.0.0.1:8000/api/company/1/paiduser'
let nonpaiduserUrl = 'http://127.0.0.1:8000/api/company/1/nonpaiduser'

let getNoPlanUser = () => {

    fetch(noplanuserUrl)
        .then(response => response.json())
        .then(data => {

            buildUserdata(data, 'noplanuser')
        })

}

let getPaidUser = () => {

    fetch(paiduserUrl)
        .then(response => response.json())
        .then(data => {

            buildUserdata(data, 'paiduser')
        })

}

let getNonPaidUser = () => {

    fetch(nonpaiduserUrl)
        .then(response => response.json())
        .then(data => {

            buildUserdata(data, 'nonpaiduser')
        })

}

let buildUserdata = (users, table_name) => {
    let target_table = document.getElementById(table_name)
    if (table_name == 'noplanuser') {

      for (let i = 0; users.length > i; i++) {
          let user = users[i]
          let table_data = `
                  <tr>
                    <td>${user.name}</td>
                    <td>${user.primary_phone_number}</td>
                    <td>${user.created.substr(0,10)} (YYYY-MM-DD)</td>
                  </tr>
          `
          target_table.innerHTML += table_data
      }


    }else if (table_name == 'paiduser') {

      for (let i = 0; users.length > i; i++) {
          let user = users[i]
          let table_data = `
                  <tr>
                    <td>${user.name}</td>
                    <td>${user.primary_phone_number}</td>
                    <td>${user.created.substr(0,10)} (YYYY-MM-DD)</td>
                    <td>${user.plan}</td>
                    <td>${user.updated.substr(0,10)} (YYYY-MM-DD)</td>
                    <td>${user.available_balance}</td>
                  </tr>
          `
          target_table.innerHTML += table_data
      }
    }else {
      for (let i = 0; users.length > i; i++) {
          let user = users[i]
          let table_data = `
                  <tr>
                    <td>${user.name}</td>
                    <td>${user.primary_phone_number}</td>
                    <td>${user.created.substr(0,10)} (YYYY-MM-DD)</td>
                    <td>${user.plan}</td>
                    <td>${user.updated.substr(0,10)} (YYYY-MM-DD)</td>
                    <td>${user.available_balance}</td>
                    <td class="charge--userplan" data-userid="${user.id}">Charge Now</td>
                    <td class="cancel--userplan" data-userid="${user.id}">Cancel Now</td>
                  </tr>
          `
          target_table.innerHTML += table_data
      }
    }


    makeChargeEvents()
    cancelEvents()
    //Add an listener
}

let makeChargeEvents = () => {
    let chargeBtns = document.getElementsByClassName('charge--userplan')

    for (let i = 0; chargeBtns.length > i; i++) {

        chargeBtns[i].addEventListener('click', (e) => {
            let userid = e.target.dataset.userid


            fetch(`http://127.0.0.1:8000/api/company/1/user/${userid}/charge`)
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data)
                    alert(data)
                })

        })
    }
}

let cancelEvents = () => {
    let cancelBtns = document.getElementsByClassName('cancel--userplan')

    for (let i = 0; cancelBtns.length > i; i++) {

        cancelBtns[i].addEventListener('click', (e) => {
            let userid = e.target.dataset.userid


            fetch(`http://127.0.0.1:8000/api/company/1/user/${userid}/cancel`)
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data)
                    alert(data)
                })

        })
    }
}


getNoPlanUser()
getPaidUser()
getNonPaidUser()
