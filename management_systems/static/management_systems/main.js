
    function showLoggedUserProfile() {
        let element = document.getElementById('logged-user-card')

        if (element.style.display === 'none') {
            element.style.display = 'flex'
        } else {
            element.style.display = 'none'
        }
    }

    function mouseEnterProfileButton() {
        let element = document.getElementById('profile-info-button')
        element.classList.remove(('fa-2x'))
        element.classList.add('fa-3x')
    }

    function mouseLeaveProfileButton() {
        let element = document.getElementById('profile-info-button')
        element.classList.remove(('fa-3x'))
        element.classList.add('fa-2x')
    }

    function showEditButton(event) {
        let id = event.target.id.substr(event.target.id.length - 1, event.target.id.length)
        console.log(id)
        document.getElementById(`edit-button${id}`).style.visibility = 'visible'
        document.getElementById(`delete-button${id}`).style.visibility = 'visible'
    }

    function hideEditButton(event) {
        let id = event.target.id.substr(event.target.id.length - 1, event.target.id.length)
        console.log(id)
        document.getElementById(`edit-button${id}`).style.visibility = 'hidden'
        document.getElementById(`delete-button${id}`).style.visibility = 'hidden'
    }

    function buttonOnHover(id) {
        id.style.background = '#0d6efd';
        id.style.cursor = 'pointer'
        id.style.color = 'white'
    }
    function buttonOffHover(id) {
        id.style.background = 'gray';
        id.style.color = '#212529'
    }

