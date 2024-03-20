function load() {
  const resultSection = document.querySelector('#result-section')
  const parentContainer = document.querySelector('.treatments-container')
  const treatmentsSections = document.querySelectorAll('.treatments')
  const minTreatmentSection = document.querySelector('.min-treatment')
  const form = document.querySelector('#diagnostic-form')
  const result = {
    treatments: [],
    min: []
  }

  function appendTreatments(treatments, element) {
    const ul = document.createElement('ul')
    ul.classList.add('list-unstyled')
    let total = 0

    for (const t of treatments) {
      ul.innerHTML += `
        <li>
          (${t.number}) ${t.drug.name} : <span class="price">${t.price}</span>€
        </li>
      `
      total += Math.round(t.price)
    }
    ul.innerHTML += `<li>Total : <span class="total">${total}</span>€</li>`

    ul.innerHTML += '<hr class="my-3"/>'

    element.appendChild(ul)
  }

  function loadResult() {
    const span = document.createElement('span')
    span.classList.add(...['bi', 'bi-info-circle-fill', 'fs-1', 'me-3'])
    minTreatmentSection.innerHTML = ''
    minTreatmentSection.appendChild(span)
    appendTreatments(result.min, minTreatmentSection)

    document.querySelectorAll('.treatments-container').forEach((el) => {
      el.innerHTML = ''
      for (const treatments of result.treatments) {
        appendTreatments(treatments, el)
      }
    })

    setTimeout(() => {
      showLoaded()
    }, 1500)
  }

  function showLoading() {
    form.classList.add('submitting')
    resultSection.classList.remove('d-none')
    resultSection.classList.remove('loaded')
    resultSection.classList.remove('empty')
    resultSection.classList.add('loading')
    const button = form.querySelector('[type="submit"]')
    button.setAttribute('disabled', true)
    button.innerHTML = 'Analyse en cours...'
  }

  function showLoaded() {
    form.classList.remove('submitting')
    resultSection.classList.remove('d-none')
    resultSection.classList.remove('loading')
    resultSection.classList.remove('empty')
    resultSection.classList.remove('error')
    resultSection.classList.add('loaded')
    const button = form.querySelector('[type="submit"]')
    button.removeAttribute('disabled')
    button.innerHTML = 'Lancer un diagnostic'
  }

  function showEmptyResult() {
    form.classList.remove('submitting')
    resultSection.classList.remove('d-none')
    resultSection.classList.remove('loaded')
    resultSection.classList.remove('loading')
    resultSection.classList.remove('error')
    resultSection.classList.add('empty')
    const button = form.querySelector('[type="submit"]')
    button.removeAttribute('disabled')
    button.innerHTML = 'Lancer un diagnostic'
  }

  function showErrorResult() {
    form.classList.remove('submitting')
    resultSection.classList.remove('d-none')
    resultSection.classList.remove('loaded')
    resultSection.classList.remove('loading')
    resultSection.classList.remove('empty')
    resultSection.classList.add('error')
    const button = form.querySelector('[type="submit"]')
    button.removeAttribute('disabled')
    button.innerHTML = 'Lancer un diagnostic'
  }

  resultSection.classList.remove('loaded')
  resultSection.classList.add('loading')

  form.onsubmit = async (e) => {
    e.preventDefault()

    const data = {
      csrfmiddlewaretoken: formData.get('csrfmiddlewaretoken'),
      name: formData.get('name'),
      selected_diseases: selectedDiseases
    }

    try {
      showLoading()
      loadDiagnostic(data)
        .then((res) => res.json())
        .then((res) => {
          result.treatments = res.result
          result.min = res.min
          loadResult()
          sortByPrice()
        })
        .catch((err) => {
          console.log(err)
          showErrorResult()
        })
    } catch (error) {
      console.log(error)
      setTimeout(() => {
        showEmptyResult()
      }, 1500)
    }
  }

  treatmentsSections.forEach((treatmentsSection) => {
    let price = 0
    treatmentsSection
      .querySelectorAll('.price')
      .forEach((priceEl) => (price += Number(priceEl.innerText)))
    treatmentsSection
      .querySelectorAll('.total')
      .forEach((totalEl) => (totalEl.innerText = price))
  })

  function sortByPrice() {
    let nodeArray = Array.prototype.slice.call(treatmentsSections)
    // parentContainer.innerHTML = ''

    nodeArray.sort((a, b) => {
      const aValue = a.querySelector('.total').textContent
      const bValue = b.querySelector('.total').textContent
      return aValue.localeCompare(bValue)
    })

    nodeArray.forEach((node) => {
      parentContainer.appendChild(node)
    })
  }

  sortByPrice()

  setTimeout(() => {
    resultSection.classList.remove('loading')
    resultSection.classList.add('loaded')
  }, 1500)

  // Format the disease select
  const name = document.querySelector('[name="name"]')
  const diseaseSelect = document.querySelector('[name="selected_diseases"]')
  const diseaseValuesInput = document.querySelector('[name="disease_values"]')
  diseaseValuesInput.classList.add('form-control-lg')
  const addDiseaseButton = document.createElement('button')
  const symptomsElements = document.querySelectorAll('.symptoms')
  const formData = new FormData(form)
  formData.set('selected_diseases', JSON.stringify({}))
  const selectedDiseases = {}

  addDiseaseButton.setAttribute('type', 'button')
  addDiseaseButton.setAttribute('title', 'Add')
  addDiseaseButton.classList.add(
    'btn',
    'btn-light',
    'btn-sm',
    'bi',
    'bi-arrow-return-left',
    'position-absolute',
    'top-0',
    'end-0',
    'mt-2',
    'me-4'
  )

  const div0 = document.createElement('div')
  const div1 = document.createElement('div')
  const div2 = document.createElement('div')

  div0.classList.add('row')
  div1.classList.add('col-5')
  div2.classList.add('col-7')

  div1.classList.add('position-relative')

  diseaseSelect.classList.add('form-select-lg')
  diseaseSelect.after(div0)
  div1.appendChild(diseaseValuesInput)
  div1.appendChild(addDiseaseButton)
  div2.appendChild(diseaseSelect)

  div0.appendChild(div2)
  div0.appendChild(div1)

  function watchDisease() {
    if (
      !diseaseSelect.value ||
      !diseaseValuesInput.value ||
      diseaseValuesInput.value <= 0
    ) {
      addDiseaseButton.setAttribute('disabled', 'disabled')
    } else {
      addDiseaseButton.removeAttribute('disabled')
    }
  }

  watchDisease()

  function getDiseaseLabel(diseaseId) {
    for (let i = 0; i < diseaseSelect.options.length; i++) {
      const option = diseaseSelect.options.item(i)
      if (option.value === diseaseId) {
        return option.label
      }
    }
    return null
  }

  function unselectDisease(diseaseId) {
    // data[diseaseId] = undefined
    delete selectedDiseases[diseaseId]
    updateSymptoms()
  }

  window.unselectDisease = unselectDisease

  function updateSymptoms() {
    symptomsElements.forEach((symptomsElement) => {
      symptomsElement.innerHTML = ''
      Object.keys(selectedDiseases).forEach((diseaseId, index) => {
        const value = Object.values(selectedDiseases)[index]
        const label = getDiseaseLabel(diseaseId)
        symptomsElement.innerHTML += `<div class="badge rounded-pill text-bg-light bg-opacity-75 text-muted align-items-center me-1 mb-1">${label} (${value}) <button type="button" onclick="window.unselectDisease(${diseaseId})" title="Remove" class="btn btn-sm bi bi-x"></button></div>`
      })
    })
  }

  diseaseSelect.onchange = (e) => {
    watchDisease()
  }

  diseaseValuesInput.oninput = (e) => {
    watchDisease()
  }

  function addDisease() {
    const diseaseId = Number(diseaseSelect.value)
    const diseaseValue = Number(diseaseValuesInput.value)
    selectedDiseases[diseaseId] = diseaseValue
    // diseaseValuesInput.value = null
    updateSymptoms()
    watchDisease()
  }

  function addSymptom(diseaseId, diseaseValue) {
    selectedDiseases[diseaseId] = diseaseValue
    // diseaseValuesInput.value = null
    updateSymptoms()
    watchDisease()
  }

  diseaseValuesInput.onkeydown = (e) => {
    if (e.keyCode === 13) {
      e.preventDefault()
      addDisease()
    }
  }

  addDiseaseButton.onclick = (e) => {
    addDisease()
  }

  async function loadDiagnostic(data) {
    let params = '?'

    params += 'name=' + data.name

    params += '&symptoms={'

    Object.keys(data.selected_diseases).forEach((key, index) => {
      const value = Object.values(data.selected_diseases)[index]
      params += key + ':' + value + ', '
    })

    params += '}'

    console.log(params)

    return fetch('/diagnostic/result' + params, {
      method: 'GET',
      headers: {
        accept: 'application/json'
      }
      // body: data
    })
  }

  // A supprimer
  // addSymptom(1, 5)
  // addSymptom(2, 5)
  // addSymptom(3, 5)
}

document.addEventListener('turbolinks:load', (e) => {
  load()
})

load()
