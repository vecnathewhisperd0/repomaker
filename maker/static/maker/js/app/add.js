/**
 * Add
 */
var buttonAdd = document.getElementById('rm-app-card-footer-action')

// Apps to be added when user click "Done"
var appsToAdd = []

// Keys for HTML5 session storage
var sessionStorageKeyApps = 'rmAppsToAdd'
var sessionStorageKeyRepo = 'rmRepo'

// Repo ID
window.repoId = '0'

// Get apps to add from local storage
if (typeof(Storage) !== "undefined") {
    var sessionStorageAppsToAdd = JSON.parse(sessionStorage.getItem(sessionStorageKeyApps))
    if (sessionStorageAppsToAdd !== null && sessionStorageAppsToAdd.length !== 0 && appsToAdd.length === 0) {
        appsToAdd = sessionStorageAppsToAdd
        markAppsToAdd()
        updateAppsToAddCount()
    }
}

function addRemoteApp(event, repoId, appRepoId, appId) {
    // Prevent opening new page
    event.preventDefault()

    if (window.repoId === '0') {
        window.repoId = repoId
        sessionStorage.setItem(sessionStorageKeyRepo, repoId)
    }
    else if (window.repoId !== repoId) {
        throw new Error('Repository ID where the apps should be added to differs')
    }

    var app = {
        appRepoId: appRepoId,
        appId: appId
    }
    var element = 'rm-app-card-footer-action--' + appId
    var appAlreadyAdded = false

    // Check if app is already to be added
    for(var i = 0; i < appsToAdd.length; i++) {
        if (appsToAdd[i].appRepoId == appRepoId && appsToAdd[i].appId == appId) {
            appAlreadyAdded = true
            appsToAdd.splice(i, 1)
            buttonSetNormal(element)
            break
        }
    }
    if (!appAlreadyAdded) {
        appsToAdd.push(app)
        buttonSetAdded(element)
    }

    // Synchronize JS with session storage
    if (typeof(Storage) !== "undefined") {
        sessionStorage.setItem(sessionStorageKeyApps, JSON.stringify(appsToAdd))
        updateAppsToAddCount()
    }
}

function back(event) {
    if (appsToAdd.length === 0) {
        return
    }
    if (window.repoId === '0') {
        window.repoId = sessionStorage.getItem(sessionStorageKeyRepo)
    }
    // Prevent opening new page
    event.preventDefault()

    var url = '/repo/' + window.repoId + '/app/add/'
    var request = new XMLHttpRequest()
    request.onreadystatechange = function() {
        if (request.readyState === 4) {
            appsAdded(request)
        }
    }
    request.open("POST", url, true) // true for asynchronous
    request.setRequestHeader("X-CSRFToken", document.getElementsByName('csrfmiddlewaretoken')[0].value)
    request.setRequestHeader('X-REQUESTED-WITH', 'XMLHttpRequest') // For Django's request.is_ajax()
    request.send(JSON.stringify(appsToAdd))
}

function appsAdded(request) {
    if (request.status === 204) {
        // Clear session storage list
        if (typeof(Storage) !== "undefined") {
            sessionStorage.removeItem(sessionStorageKeyApps)
            sessionStorage.removeItem(sessionStorageKeyRepo)
        }

        window.location = '/repo/' + window.repoId
    }
    else {
        showError(request.responseText)
    }
}

function markAppsToAdd() {
    for (var i = 0; i < appsToAdd.length; i++) {
        var element = 'rm-app-card-footer-action--' + appsToAdd[i]['appId']
        buttonSetAdded(element)
    }
}

function updateAppsToAddCount() {
    var count = appsToAdd.length
    var countContainer = document.querySelector('.rm-repo-add-toolbar-count')
    countContainer.hidden = false
    var countText = document.getElementById('rm-repo-add-toolbar-count-text')
    if (count > 0) {
        countText.textContent =
            interpolate(ngettext('%s app added', '%s apps added', count), [count])
    }
    else {
        countContainer.hidden = true
    }
}

function clearAppsToAdd(event) {
    // Clear session storage list
    if (typeof(Storage) !== "undefined") {
        sessionStorage.removeItem(sessionStorageKeyApps)
    }
}

function buttonSetAdded(element) {
    setClassOfElement(element, 'rm-app-card-footer-action--successful')
    setContentOfElement(element + '-button', '<i class="material-icons">done</i>')
}

function buttonSetNormal(element) {
    setClassOfElement(element, 'rm-app-card-footer-action')
    setContentOfElement(element + '-button', gettext('Add'))
}

function showError(text) {
    var element = 'rm-app-add-errors'
    setContentOfElement(element, text)
    setHiddenOfElement(element, false)
}

/**
 * Miscellaneous
 */
function setClassOfElement(element, myClass) {
    element = document.getElementById(element)
    if (element !== null) {
        element.className = myClass
    }
}

function setContentOfElement(element, content) {
    element = document.getElementById(element)
    if (element !== null) {
        element.innerHTML = content
    }
}

function setHiddenOfElement(element, hidden) {
    if (typeof element === 'string') {
        element = document.getElementById(element)
    }
    if (element !== null) {
        element.hidden = hidden
    }
}

/**
 * Pagination
 */
var rmPaginationPage = null

var mdlBody = document.querySelector('.mdl-layout__content')
mdlBody.addEventListener("scroll", function () {
    if (mdlBody.scrollHeight - window.innerHeight -
            mdlBody.scrollTop <= 800) {
        var pagination = document.querySelector('.rm-pagination')
        if (pagination !== null) {
            handlePagination(pagination, window.location.href)
        }
    }
}, false)

function handlePagination(pagination, urlString) {
    if (pagination.hidden || rmPaginationPage === 0) {
        return
    }
    pagination.hidden = true
    var url = new URL(urlString)
    if (rmPaginationPage === null) {
        rmPaginationPage = 2
        // Handle case where user is on ?page=x, e.g. due to slow loading of page
        pageParam = url.searchParams.get('page')
        if (pageParam !== null && pageParam.length !== 0) {
            rmPaginationPage = parseInt(pageParam) + 1
        }
    }
    searchParam = url.searchParams.get('search')
    if (searchParam === null || searchParam.length === 0) {
        urlString = urlString.split('?')[0] + '?page=' + rmPaginationPage
    }
    else {
        urlString = urlString.split('?')[0] + '?search=' + searchParam + '&page=' + rmPaginationPage
    }
    var request = new XMLHttpRequest()
    request.onreadystatechange = function() {
        if (request.readyState === 4) {
            if (request.status !== 404) {
                appendApps(request)
                pagination.hidden = false
                rmPaginationPage = rmPaginationPage + 1
            }
            else {
                rmPaginationPage = 0
            }
        }

    }
    request.open("GET", new URL(urlString), true) // true for asynchronous
    request.setRequestHeader('X-REQUESTED-WITH', 'XMLHttpRequest') // For Django's request.is_ajax()
    request.send()
}

function appendApps(request) {
    var apps = JSON.parse(request.response)
    var appList = document.querySelector('.rm-app-add-apps')
    var appCardTemplate = document.querySelector('.rm-app-card')
    for (app in apps) {
        var newAppCard = appCardTemplate.cloneNode(true)
        newAppCard = putAppInformation(apps[app], newAppCard)
        appList.appendChild(newAppCard)
    }
}

var jsonHtmlRelation = {
    'rm-app-card-title': 'name',
    'rm-app-card-summary': 'summary',
    'rm-app-card-description': 'description',
    'rm-app-card-updated': 'last_updated_date',
    'rm-app-card-left': 'icon',
    'rm-app-card-footer-action': 'id',
    'rm-app-card-categories': 'categories',
}

function putAppInformation(app, appCard) {
    for (rel in jsonHtmlRelation) {
        if (rel === 'rm-app-card-updated') {
            date = new Date(app[jsonHtmlRelation[rel]])
            appCard.querySelector('.' + rel).innerHTML = formatDate(date)
            continue
        }
        if (rel === 'rm-app-card-left') {
            appCard.querySelector('.' + rel).style.backgroundImage =
                'url("/media/' + app[jsonHtmlRelation[rel]] + '")'
            continue
        }
        if (rel === 'rm-app-card-description') {
            // Strip HTML and truncate
            appCard.querySelector('.' + rel).innerHTML =
                app[jsonHtmlRelation[rel]].replace(/<(?:.|\n)*?>/gm, '').substring(0, 168) + '...'
            continue
        }
        if (rel === 'rm-app-card-footer-action') {
            var appId = app[jsonHtmlRelation[rel]]
            var element = appCard.querySelector('.' + rel)

            // Set ID
            element.id = rel + '--' + appId

            var repoId = element.pathname.split('/')[2]
            var remoteRepoId = app['repo_id']

            // Set link
            element.href = '/repo/' + repoId + '/app/remote/' + remoteRepoId + '/add/' + appId

            // Add on-click listener and remove HTML attribute
            element.addEventListener('click', function(event) {
                addRemoteApp(event, repoId, remoteRepoId, appId)
            })
            element.removeAttribute('onclick')

            // Set ID of button
            element.querySelector('button').id = rel + '--' + appId + '-button'
            continue
        }
        if (rel === 'rm-app-card-categories') {
            // TODO: Add categories
            var nodes = appCard.querySelector('.' + rel).childNodes;
            for(var i = 0; i < nodes.length; i++) {
                console.log
                nodes[i].hidden = true
            }
            continue
        }
        appCard.querySelector('.' + rel).innerHTML = app[jsonHtmlRelation[rel]]
    }
    return appCard
}

function formatDate(date) {
    var monthNames = [
        "Jan.", "Feb.", "March",
        "April", "May", "June", "July",
        "Aug.", "Sep.", "Oct.",
        "Nov.", "Dec."
    ];

    var day = date.getDate();
    var monthIndex = date.getMonth();
    var year = date.getFullYear();

    return monthNames[monthIndex] + ' ' + day + ', ' + year;
}

/**
 * Search
 */
var searchInput = document.querySelector('.rm-app-add-filters-search-input')
var searchClear = document.querySelector('.rm-app-add-filters-search-clear')

// Set hidden or not at page load
setHiddenOfElement(searchClear, (searchInput.value.length === 0))

// Set hidden or not on input
searchInput.addEventListener("input", function() {
    setHiddenOfElement(searchClear, (searchInput.value.length === 0))
})
