Vue.component('new-input', {
    template: `
        <div>
            <form id="input-form">
                <div v-for="input in inputFields">
                    <label><span data-tooltip aria-haspopup="true" class="has-tip" data-disable-hover='false' tabindex=1 :title="input.help">{{ input.name }}</span>: <span v-if=input.required style="color: red;">*</span>
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
            name: 'name',
            required: true,
            type: 'text',
            value: '',
            defaultValue: '',
            help: 'Give the input parameter a name that will be used in the code for the app.',
        }, {
            name: 'label',
            required: true,
            type: 'text',
            value: '',
            defaultValue: '',
            help: 'Give the input parameter a label which will be shown in the UI when configuring the app.',
        }, {
            name: 'type',
            required: true,
            type: 'text',
            value: 'String',
            defaultValue: 'String',
            possibleValues: ['Boolean', 'Choice', 'KeyValueList', 'MultiChoice', 'String', 'StringMixed'], // todo: do something when the value of this changes - modify the other displayed values (3)
            keepIfDefault: true,
            help: 'Specify the type of the input parameter. This will determine which UI input element is used when configuring the app.',
        }, {
            name: 'allowMultiple',
            required: false,
            type: 'checkbox',
            value: false,
            defaultValue: false,
            // todo: add a better description to the help message below... I'm not exactly sure what the allowMultiple does (3)
            help: 'Choose to allow multiple inputs for this input parameter.',
        }, {
            name: 'default (as a boolean)',
            required: false,
            type: 'checkbox',
            value: false,
            defaultValue: false,
            help: 'Give the input parameter a default value.',
        }, {
            name: 'default (as a string/integer)',
            required: false,
            type: 'text',
            value: '',
            defaultValue: '',
            help: 'Give the input parameter a default value.',
        }, {
            name: 'encrypt',
            required: false,
            type: 'checkbox',
            value: false,
            defaultValue: false,
            help: 'Choose to encrypt the input value (useful for passwords, API keys, and other sensitive values).',
        }, {
            name: 'hidden',
            required: false,
            type: 'checkbox',
            value: false,
            defaultValue: false,
            // todo: make sure the help message below is accurate (3)
            help: 'Choose to hide this input parameter in the UI when configuring the app.',
        }, {
            name: 'note',
            required: false,
            type: 'text',
            value: '',
            defaultValue: '',
            // TODO: not sure what this value does (3)
            help: 'Not sure what this does yet...',
        }, {
            name: 'playbookDataType',
            required: false,
            type: 'text',
            value: '',
            defaultValue: '',
            possibleValues: ['Any', 'Binary', 'BinaryArray', 'KeyValue', 'KeyValueArray', 'String', 'StringArray', 'TCEntity', 'TCEntityArray'],
            multiple: true,
            // TODO: not sure what this value does (3)
            help: 'Not sure what this does yet...',
        }, {
            name: 'required',
            required: false,
            type: 'checkbox',
            value: false,
            defaultValue: false,
            help: 'Choose to make the input parameter required.',
        }, {
            name: 'sequence',
            required: false,
            type: 'number',
            value: undefined,
            defaultValue: undefined,
            help: 'Specify the order in which this input parameter will be listed when configuring the playbook. Lower numbers are listed first and higher numbers are listed later',
        }, {
            name: 'validValues',
            required: false,
            type: 'text',
            value: '',
            defaultValue: '',
            help: 'This limits the number of possible values for this input parameter. If you want to have multiple values, separate them with a semi-colon (";").'
        }, {
            name: 'viewRows',
            required: false,
            type: 'number',
            value: undefined,
            defaultValue: undefined,
            // TODO: not sure what this value does (3)
            help: 'Not sure what this does yet...',
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
        handleValidValues: function(validValuesString) {
            /* Create an array out of a semi-colon delimited string given for the valid values. */
            return validValuesString.split(";").map(x => x.trim());
        },
        handleDefaultValues: function(defaultString) {
            /* Check to see if the given, default value should be converted to a number or not. */
            if (Number(defaultString)) {
                return Number(defaultString);
            } else {
                return defaultString;
            }
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
                    if (this.inputFields[i].name === 'validValues') {
                        inputObject[this.inputFields[i].name] = this.handleValidValues(this.inputFields[i].value);
                    } else if (this.inputFields[i].name.split(" (")[0] === 'default') {
                        // check to make sure there is not already a default value
                        if (inputObject['default']) {
                            $.jGrowl('There is already a default value. Two default values cannot be added.', {group: 'warning-growl'});
                        } else {
                            if (this.inputFields[i].value === true) {
                                inputObject[this.inputFields[i].name.split(" (")[0]] = this.inputFields[i].value;
                            } else {
                                inputObject[this.inputFields[i].name.split(" (")[0]] = this.handleDefaultValues(this.inputFields[i].value);
                            }
                        }
                    } else {
                        inputObject[this.inputFields[i].name] = this.inputFields[i].value;
                    }
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
                    <label><span data-tooltip aria-haspopup="true" class="has-tip" data-disable-hover='false' tabindex=1 :title="output.help">{{ output.name }}</span>: <span v-if=output.required style="color: red;">*</span>
                    <input v-if="!output.possibleValues" :type=output.type name="label" v-model="output.value">
                    <select v-if="output.possibleValues && !output.multiple" v-model="output.value">
                      <option v-for="option in output.possibleValues">{{ option }}</option>
                    </select></label>
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
            help: 'This is the name of the output variable that will be made available to downstream apps.'
        }, {
            name: 'type',
            required: true,
            type: 'text',
            value: 'String',
            defaultValue: 'String',
            possibleValues: ['Any', 'Binary', 'BinaryArray', 'KeyValue', 'KeyValueArray', 'String', 'StringArray', 'TCEntity', 'TCEntityArray'],
            help: 'This specifies the type of the output variable. Depending on which type you choose, it can limit which downstream apps have access to the variable.'
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
