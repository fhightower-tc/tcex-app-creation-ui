Vue.component('new-input', {
    template: `
        <div>
            <form id="input-form">
                <div v-for="input in inputFields">
                    <label>{{ input.name }}: <span v-if=input.required style="color: red;">*</span>
                    <input v-if="!input.possibleValues" :type=input.type name="label" v-model="input.value">
                    <select v-if="input.multiple" v-model="input.value" multiple>
                      <option v-for="option in input.possibleValues">{{ option }}</option>
                    </select>
                    <select v-if="input.possibleValues && !input.multiple" v-model="input.value">
                      <option v-for="option in input.possibleValues">{{ option }}</option>
                    </select></label>
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
            defaultValue: '',
        }, {
            name: 'name',
            required: true,
            type: 'text',
            value: '',
            defaultValue: '',
        }, {
            name: 'type',
            required: true,
            type: 'text',
            value: 'String',
            defaultValue: 'String',
            possibleValues: ['Boolean', 'Choice', 'KeyValueList', 'MultiChoice', 'String', 'StringMixed'], // todo: do something when the value of this changes - modify the other displayed values
            keepIfDefault: true,
        }, {
            name: 'allowMultiple',
            required: false,
            type: 'checkbox',
            value: false,
            defaultValue: false,
        }, {// TODO: add handling for default - this value can be one of many different types (strings, bools, etc.)
            name: 'default',
            required: false,
            type: 'checkbox',
            value: false,
            defaultValue: false,
        }, {
            name: 'encrypt',
            required: false,
            type: 'checkbox',
            value: false,
            defaultValue: false,
        }, {
            name: 'hidden',
            required: false,
            type: 'checkbox',
            value: false,
            defaultValue: false,
        }, {
            name: 'note',
            required: false,
            type: 'text',
            value: '',
            defaultValue: '',
        }, {
            name: 'playbookDataType',
            required: false,
            type: 'text',
            value: '',
            defaultValue: '',
            possibleValues: ['Any', 'Binary', 'BinaryArray', 'KeyValue', 'KeyValueArray', 'String', 'StringArray', 'TCEntity', 'TCEntityArray'],
            multiple: true,
        }, {
            name: 'required',
            required: false,
            type: 'checkbox',
            value: false,
            defaultValue: false,
        }, {
            name: 'sequence',
            required: false,
            type: 'number',
            value: undefined,
            defaultValue: undefined,
        }, {// TODO: add better handling here...
            name: 'validValues',
            required: false,
            type: 'text',
            value: '',
            defaultValue: '',
        }, {
            name: 'viewRows',
            required: false,
            type: 'number',
            value: undefined,
            defaultValue: undefined,
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
        resetValues: function() {
            /* Reset the values of every entry. */
            for (var i = this.inputFields.length - 1; i >= 0; i--) {
                this.inputFields[i].value = this.inputFields[i].defaultValue;
            }
        },
        addParameter: function() {
            /* Prepare the input object as an object. */
            if (!this.validInputs()) {
                return;
            }

            var inputObject = {};

            for (var i = this.inputFields.length - 1; i >= 0; i--) {
                if (this.inputFields[i].value !== this.inputFields[i].defaultValue || this.inputFields[i].keepIfDefault) {
                    inputObject[this.inputFields[i].name] = this.inputFields[i].value;
                }
            }

            playbookAppVue.parameters.push(inputObject);

            // reset the form
            document.getElementById('input-form').reset();
            this.resetValues();
        },
    }
});

Vue.component('new-output', {
    template: `
        <div>
            <form id="output-form">
                <div v-for="output in outputFields">
                    <label>{{ output.name }}: <span v-if=output.required style="color: red;">*</span><input :type=output.type name="label" v-model=output.value></label>
                </div>
            </form>
            <button class="button secondary" v-on:click="addOutputVariable">Add parameter</button>
        </div>
    `,
    data: function () {
      return {
        outputFields: [{
            name: 'name',
            required: true,
            type: 'text',
            value: '',
            defaultValue: '',
        }, {// TODO: add better handling for type
            name: 'type',
            required: true,
            type: 'text',
            value: '',
            defaultValue: '',
        }],
      };
    },
    methods: {
        validOutputs: function() {
            /* Make sure all of the required outputs are present. */
            for (var i = 0; i <= this.outputFields.length - 1; i++) {
                if (this.outputFields[i].required && this.outputFields[i].value == '') {
                    $.jGrowl(`Missing required output parameter: ${this.outputFields[i].name}`, {group: 'failure-growl'});
                    return false;
                }
            }
            return true;
        },
        resetValues: function() {
            /* Reset the values of every entry. */
            for (var i = this.outputFields.length - 1; i >= 0; i--) {
                this.outputFields[i].value = this.outputFields[i].defaultValue;
            }
        },
        addOutputVariable: function() {
            /* Prepare the output object as an object. */
            if (!this.validOutputs()) {
                return;
            }

            var outputObject = {};

            for (var i = this.outputFields.length - 1; i >= 0; i--) {
                outputObject[this.outputFields[i].name] = this.outputFields[i].value;
            }

            playbookAppVue.outputVariables.push(outputObject);

            // reset the form
            document.getElementById('output-form').reset();
            this.resetValues();
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
