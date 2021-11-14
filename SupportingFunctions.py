def warnings():
    from IPython.display import HTML
    HTML('''<script>
    code_show_err=false;
    function code_toggle_err() {
     if (code_show_err){
     $('div.output_stderr').hide();
     } else {
     $('div.output_stderr').show();
     }
     code_show_err = !code_show_err
    }
    $( document ).ready(code_toggle_err);
    </script>
    To toggle on/off for showing warnings, click <a href="javascript:code_toggle_err()">here</a>.''')

def nice_print(ListOfFiles):
    print("\n")
    for x in range(len(ListOfFiles)):
        print("\t-", ListOfFiles[x], end = " ")
        print("\n")

def ask_dir():
    from ij.io import OpenDialog
    op = OpenDialog("Choose Track Data...", "")
    print(op.getDirectory()+ op.getFileName())
