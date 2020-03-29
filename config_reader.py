def is_field(cfg, word):
    if word == '':
        return 0
    if word[0] != cfg.field_begin:
        return 0
    if word[-1] != cfg.field_end:
        return 0
    return 1

class config:
    def __init__(self, filename, eol='\n', field_begin='[', field_end=']', autogenerate=True):
        self.filename = filename
        self.eol = eol
        self.field_begin = field_begin
        self.field_end = field_end
        self.words = [""]
        if autogenerate:
            self.config_reader(self.filename)
    def config_reader(self, filename):
        self.filename = filename
        with open(self.filename, "r") as fp:
            text = fp.read()
            for c in text:
                if c == self.eol:
                    if self.words[-1] != '':
                        self.words.append(self.eol)
                        self.words.append("")
                    else:
                        self.words[-1] = self.eol
                        self.words.append("")
                    continue
                if c == ' ':
                    if self.words[-1] != '':
                        self.words.append("")
                    continue
                self.words[-1] += c
        print(self.words)
    def get_field(self, fieldname):
        field = []
        looking_for = '[' + fieldname + ']'
        start = 0
        found = False
        for w in self.words:
            start+=1
            if w == looking_for:
                found = True
                break
        if not found:
            return ["FAILEDTOFETCH: " + looking_for]
        while not is_field(self, self.words[start]):
            field.append(self.words[start])
            start+=1
            if start >= len(self.words):
                return ["FAILEDTOFETCH: " + looking_for]
        return field
    def get_val(self, field, valname):
        val = []
        after_eol = False
        start = 0
        for w in field:
            start+=1
            if w == valname and after_eol:
                val.append([])
                for i in range(start, len(field)):
                    if field[i] == '\n' and not is_field(cfg, field[i]):
                        break
                    val[-1].append(field[i])
            if w == self.eol:
                after_eol = True
        return val

    def get_last_val(self, field, valname):
        val = self.get_val(field, valname)
        if len(val) == 0:
            return val
        else:
            return val[-1]
    def get_first_val(self, field, valname):
        val = self.get_val(field, valname)
        if len(val) == 0:
            return val
        else:
            return val[0]
        
    def dir_get_val(self, fieldname, valname):
        field = self.get_field(fieldname)
        return self.get_val(field, valname)    
    def dir_get_last_val(self, fieldname, valname):
        field = self.get_field(fieldname)
        return self.get_last_val(field, valname)
    def dir_get_first_val(self, fieldname, valname):
        field = self.get_field(fieldname)
        return self.get_first_val(field, valname)
            
if __name__ == "__main__":
    import sys
    filename = ""
    if len(sys.argv) < 2:
        filename = "example.cfg"
    elif len(sys.argv) < 3 and sys.argv[0][:6] == "python":
        filename = "example.cfg"
    elif sys.argv[0][:6] == "python":
        filename = sys.argv[2]
    else:
        filename = sys.argv[1]
    cfg = config(filename)
    cfg.config_reader(filename)
    field1 = cfg.get_field("FIELD1") 
    print("FIELD: ", field1)
    print(cfg.dir_get_last_val("FIELD1", 'MIN'))
