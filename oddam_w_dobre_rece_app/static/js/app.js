document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          if (this.validateForm()) {
          this.currentStep++;
          this.updateForm();
          }
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;


      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      if (this.currentStep === 5) {
        this.updateSummary();
      }
    }
    validateForm() {

        let isValid = true;

        if (this.currentStep == 1){
            var markedCheckbox = document.querySelectorAll('input[type=checkbox]:checked');
            if (markedCheckbox.length == 0) {
               alert("Musisz zaznaczyć co najmniej 1 kategorię.");
               isValid = false;
            }
        } else if (this.currentStep == 2) {
            const bags = document.querySelector("input[name='bags']").value;
            if (bags === "" || isNaN(bags) || bags < 1) {
                alert("Wprowadź liczbę worków nie mniejszą niż 1.");
                isValid = false;
            }
        } else if (this.currentStep == 3) {
            const org = document.querySelector("input[name='organization']:checked")
            if (org === null) {
                alert("Musisz wybrać organizację.");
                isValid = false;
            }
        } else if (this.currentStep == 4) {
            const address = document.querySelector("input[name='address']").value;
            const city = document.querySelector("input[name='city']").value;
            const postcode = document.querySelector("input[name='postcode']").value;
            const phone = document.querySelector("input[name='phone']").value;
            const data = document.querySelector("input[name='data']").value;
            const time = document.querySelector("input[name='time']").value;
            const currentDateTime = new Date();
            const selectedDateTime = new Date(`${data}T${time}`);
            if (address === "") {
                alert("Musisz podać adres.");
                isValid = false;
            } else if (city === "") {
                alert("Musisz podać miasto.");
                isValid = false;
            } else if (!/^\d{2}-\d{3}$/.test(postcode)) {
                alert("Musisz podać poprawny kod pocztowy w formacie XX-XXX.");
                isValid = false;
            } else if (!/^\d{9}$/.test(phone)) {
                alert("Musisz podać poprawny numer telefonu (9 cyfr).");
                isValid = false;
            } else if (data === "") {
                alert("Musisz podać datę odbioru.");
                isValid = false;
            } else if (time === "") {
                alert("Musisz podać godzinę odbioru.");
                isValid = false;
            } else if (selectedDateTime < currentDateTime) {
                alert("Data i godzina odbioru nie mogą być w przeszłości.");
                isValid = false;
            }
        }
        return isValid;
    }

    updateSummary() {

        const bags = document.querySelector("input[name='bags']").value;
        const categories = Array.from(document.querySelectorAll('input[type=checkbox]:checked'))
          .map(checkbox => checkbox.dataset.categoryName)
          .join(", ");

        const organization = document.querySelector("input[name='organization']:checked").value;

        const address = document.querySelector("input[name='address']").value;
        const city = document.querySelector("input[name='city']").value;
        const postcode = document.querySelector("input[name='postcode']").value;
        const phone = document.querySelector("input[name='phone']").value;
        const date = document.querySelector("input[name='data']").value;
        const time = document.querySelector("input[name='time']").value;
        const moreInfo = document.querySelector("textarea[name='more_info']").value || "Brak uwag";

        document.querySelector(".summary--bags-text").textContent = `${bags} worki z nastepujacymi przedmiotami: ${categories}`;
        document.querySelector(".summary--organization-text").textContent = `Dla fundacji "${organization}" w ${city}`;

        document.querySelector(".summary--address").textContent = address;
        document.querySelector(".summary--city").textContent = city;
        document.querySelector(".summary--postcode").textContent = postcode;
        document.querySelector(".summary--phone").textContent = phone;

        document.querySelector(".summary--date").textContent = date;
        document.querySelector(".summary--time").textContent = time;
        document.querySelector(".summary--more-info").textContent = moreInfo;

    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
  e.preventDefault();

  // Zbieranie danych z formularza
  const formData = new FormData(document.querySelector('form'));
  const data = {};
  formData.forEach((value, key) => {
    if (data[key]) {
      if (!Array.isArray(data[key])) {
        data[key] = [data[key]];
      }
      data[key].push(value);
    } else {
      data[key] = value;
    }
  });

  fetch('/add-donation/form-confirmation/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      window.location.href = data.redirect;
    } else {
      alert('Wystąpił błąd: ' + data.message);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Wystąpił błąd. Spróbuj ponownie.');
  });
}

  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});


function get_ids_from_check_box() {
    var markedCheckbox = document.querySelectorAll('input[type=checkbox]:checked');
    var ids = [];
    markedCheckbox.forEach(box => ids.push(box.value));
    return ids;
}

function aport() {
    var arr = get_ids_from_check_box();
    var moj_url = '/institution-by-category?';
    var params = new URLSearchParams();
    arr.forEach(id => params.append('category_ids', id));
    var parameters = params.toString();  //parameters === type_ids=1&type_ids=2&type_ids=3
    moj_url = moj_url + parameters;

    var test = document.getElementById('organizations');
    fetch(moj_url)
        .then(response => response.json())
        .then(data => {
            while (test.firstChild) {
                test.removeChild(test.lastChild);
            }
            data.forEach(function (element) {
                const div = document.createElement('div');
                div.classList.add('form-group', 'form-group--checkbox');

                const label = document.createElement('label');

                const input = document.createElement('input');
                input.type = 'radio';
                input.name = 'organization';
                input.value = element.name;

                const spanCheckbox = document.createElement('span');
                spanCheckbox.classList.add('checkbox', 'radio');

                const spanDescription = document.createElement('span');
                spanDescription.classList.add('description');

                const divTitle = document.createElement('div');
                divTitle.classList.add('title');
                divTitle.innerText = element.name;

                const divSubtitle = document.createElement('div');
                divSubtitle.classList.add('subtitle');
                divSubtitle.innerText = 'Cel i misja: ' + element.description;

                spanDescription.appendChild(divTitle);
                spanDescription.appendChild(divSubtitle);
                label.appendChild(input);
                label.appendChild(spanCheckbox);
                label.appendChild(spanDescription);
                div.appendChild(label);
                test.appendChild(div);
            });
        });
}

document.addEventListener('DOMContentLoaded', function () {
    var checkboxs = document.querySelectorAll("input[type=checkbox]");
    checkboxs.forEach(function (checkbox) {
        checkbox.addEventListener('change', aport);
    });
});