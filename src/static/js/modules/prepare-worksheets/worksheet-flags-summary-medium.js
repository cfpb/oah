var _grades = require('./inputs/input-graded-grades');

var worksheetSettings = {
  template: require( '../../templates/prepare-worksheets/worksheet-flags-summary-medium.hbs' ),
  inputModule: require( './inputs/input-stacked-text' ),
  type: 'flags',
  skipEmpties: true,
  showOnlyGrade: _grades.MEDIUM,
  getDefaultInputOptions: _getDefaultInputOptions
};
this.worksheetSettings = worksheetSettings;

// @return [Object] Default settings for a new user input control.
function _getDefaultInputOptions() {
  return {
    inputValue: '',
    placeholder: '',
    highGradeText: '',
    mediumGradeText: '',
    lowGradeText: '',
    deletable: false
  };
}