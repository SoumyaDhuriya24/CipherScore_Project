import AceEditor from "react-ace";

import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-monokai";
import "ace-builds/src-noconflict/ext-language_tools";

const CodeEditor = ({ code, onChange }) => {
    return (
        <AceEditor
            mode="python"
            theme="monokai"
            onChange={onChange}
            value={code}
            name="UNIQUE_ID_OF_DIV"
            editorProps={{ $blockScrolling: true }}
            width="100%"
            height="400px"
            fontSize={14}
            showPrintMargin={true}
            showGutter={true}
            highlightActiveLine={true}
            setOptions={{
                enableBasicAutocompletion: true,
                enableLiveAutocompletion: true,
                enableSnippets: false,
                showLineNumbers: true,
                tabSize: 4,
                fontFamily: "var(--font-mono)",
            }}
            style={{
                borderRadius: "var(--radius-md)",
                fontFamily: "var(--font-mono)",
            }}
        />
    );
};

export default CodeEditor;
