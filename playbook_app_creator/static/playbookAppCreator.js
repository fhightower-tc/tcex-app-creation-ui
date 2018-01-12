Vue.component('new-input', {
    template: `
        <div>
            <form id="input-form">
                <div v-for="input in inputFields">
                    <label>{{ input.name }}: <span v-if=input.required style="color: red;">*</span><input :type=input.type name="label" v-model=input.value></label>
                </div>
            </form>
            <button class="button secondary" v-on:click="addParameter">Add parameter</button>
        </div>
    `,
    data: function () {
      return {
        inputFields: [{
            name: 'label',
            required: true,
            type: 'text',
            value: '',
        }, {
            name: 'name',
            required: true,
            type: 'text',
            value: '',
        }, {// TODO: add better handling for type
            name: 'type',
            required: true,
            type: 'text',
            value: '',
        }, {
            name: 'allowMultiple',
            required: false,
            type: 'checkbox',
            value: false,
        }, {// TODO: add handling for default
            name: 'default',
            required: false,
            type: 'checkbox',
            value: false,
        }, {
            name: 'encrypt',
            required: false,
            type: 'checkbox',
            value: false,
        }, {
            name: 'hidden',
            required: false,
            type: 'checkbox',
            value: false,
        }, {
            name: 'note',
            required: false,
            type: 'text',
            value: '',
        }, {// TODO: add handline for playbookDataType
            name: 'playbookDataType',
            required: false,
            type: 'text',
            value: '',
        }, {
            name: 'required',
            required: false,
            type: 'checkbox',
            value: false,
        }, {
            name: 'sequence',
            required: false,
            type: 'number',
            value: undefined,
        }, {// TODO: add better handling here...
            name: 'validValues',
            required: false,
            type: 'text',
            value: '',
        }, {// TODO: add better handling here...
            name: 'viewRows',
            required: false,
            type: 'number',
            value: undefined,
        }],
      };
    },
    methods: {
        validInputs: function() {
            /* Make sure all of the required inputs are present. */
            for (var i = 0; i <= this.inputFields.length - 1; i++) {
                if (this.inputFields[i].required && this.inputFields[i].value == '') {
                    $.jGrowl(`Missing required input: ${this.inputFields[i].name}`, {group: 'failure-growl'});
                    return false;
                }
            }
            return true;
        },
        addParameter: function() {
            /* Prepare the input object as an object. */
            if (!this.validInputs()) {
                return;
            }

            var inputObject = {};

            for (var i = this.inputFields.length - 1; i >= 0; i--) {
                inputObject[this.inputFields[i].name] = this.inputFields[i].value;
            }

            playbookAppVue.parameters.push(inputObject);

            // reset the form
            document.getElementById('input-form').reset();
        },
    }
});

var playbookAppVue = new Vue({
    el: "#content",
    data: {
        parameters: [],
        outputVariables: [],
    },
});
