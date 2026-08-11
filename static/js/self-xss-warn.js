// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

(function() {
    const mainMessage = "Hold Up!";
    const description = "If someone told you to paste something here, there is a 110% chance they are trying to steal your data. Bad things could happen.";
    
    const mainStyle = "color: red; font-size: 40px; font-weight: bold; -webkit-text-stroke: 1px black; background-color: white;";
    const subStyle = "color: #222; font-size: 16px; font-weight: 500; font-family: sans-serif; background-color: white;";

    console.log(`%c${mainMessage}`, mainStyle);
    console.log(`%c${description}`, subStyle);
})();