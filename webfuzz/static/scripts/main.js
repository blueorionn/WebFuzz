// scripts/main.js

/**
 * Returns config object to send as post body to api
 */
function postFuzzingConfig() {
    const DEFAULT_FUZZ_DELAY_VALUE = 10 // in ms
    const DEFAULT_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'

    const FUZZ_URL = document.querySelector('input#fuzz-url').value
    const FUZZ_METHOD = document.querySelector('select#http-method').value
    const FUZZ_DELAY = document.querySelector('input#fixed-delay').value || DEFAULT_FUZZ_DELAY_VALUE
    const FUZZ_FILTER_STATUS_CODES = document.querySelector('input#filter-status-codes').value
    const FUZZ_MATCH_STATUS_CODES = document.querySelector('input#match-status-codes').value
    const FUZZ_PAYLOAD = document.querySelector('textarea#payload').value
    const FUZZ_POST_DATA = document.querySelector('textarea#post-data').value
    const FUZZ_USER_AGENT = document.querySelector('input#user-agent').value || DEFAULT_USER_AGENT
    const FUZZ_COOKIES = document.querySelector('input#cookies').value

    // validate URL
    if (!isValidURL(FUZZ_URL)) {
        alert('Given URL is not valid')
        return
    }

    // validate request method
    if (!['GET', 'POST', 'PUT', 'DELETE'].includes(FUZZ_METHOD)) {
        alert(`Unsupported Method ${FUZZ_METHOD}`)
        return
    }

    // validate fuzz delay
    if (!/\d/.test(FUZZ_DELAY) || isNaN(FUZZ_DELAY) || FUZZ_DELAY === '') {
        alert('Unsupported FUZZ_DELAY value must be a number')
        return
    }

    // validate fuzz filter status code
    if (FUZZ_FILTER_STATUS_CODES !== '' && !/^\d{3},\d{3}$/.test(FUZZ_FILTER_STATUS_CODES)) {
        alert('Unsupported status code in FUZZ_FILTER_STATUS_CODES')
        return
    }

    // validate fuzz match status code
    if (FUZZ_MATCH_STATUS_CODES !== '' && !/^\d{3},\d{3}$/.test(FUZZ_MATCH_STATUS_CODES)) {
        alert('Unsupported status code in FUZZ_MATCH_STATUS_CODES')
        return
    }

    // validate payload/wordlist
    if (FUZZ_PAYLOAD === '') {
        alert('payload is empty')
        return
    }

    return {
        FUZZ_URL,
        FUZZ_METHOD,
        FUZZ_DELAY,
        FUZZ_FILTER_STATUS_CODES,
        FUZZ_MATCH_STATUS_CODES,
        FUZZ_PAYLOAD,
        FUZZ_POST_DATA,
        FUZZ_USER_AGENT,
        FUZZ_COOKIES
    }
}

async function postData(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`)
        }

        const responseData = await response.json()
    } catch (error) {
        console.error('Error:', error) // Handle network or HTTP errors
    }
}

(function () {
    const API_ENDPOINT = '/api/fuzz'
    const FUZZ_BUTTON = document.querySelector('button#send-fuzzing-request')
    FUZZ_BUTTON.addEventListener("click", function () {
        const POST_DATA = postFuzzingConfig()

        // post data to api
        if (POST_DATA !== undefined) {
            postData(API_ENDPOINT, JSON.stringify(POST_DATA))
        }
    })
})()