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
        self.generated = False
        if autogenerate:
            self.config_reader(self.filename)
            self.generated = True
    def config_reader(self, filename, regenerate=False):
        if not (self.generated == True and self.filename==filename and regenerate==False):
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
            raise BaseException("config_reader.py: get_field: failed to find field " + looking_for)
        while not is_field(self, self.words[start]):
            field.append(self.words[start])
            start+=1
            if start >= len(self.words):
                raise BaseException("config_reader.py: get_field: failed to find field " + looking_for)
        return field
    def get_attr(self, field, attr):
        val = []
        after_eol = False
        start = 0
        found = False
        for w in field:
            start+=1
            if w == attr and after_eol:
                found = True
                val.append([])
                for i in range(start, len(field)):
                    if field[i] == '\n' and not is_field(cfg, field[i]):
                        break
                    val[-1].append(field[i])
            if w == self.eol:
                after_eol = True
        if found == False:
            raise BaseException("config_reader.py: get_val: failed to find attr " + attr)
        return val

    def get_last_attr(self, field, attr):
        val = self.get_attr(field, attr)
        return val[-1]
    
    def get_first_attr(self, field, attr):
        val = self.get_attr(field, attr)
        return val[0]
        
    def dir_get_attr(self, fieldname, attr):
        field = self.get_field(fieldname)
        return self.get_attr(field, attr)    
    def dir_get_last_attr(self, fieldname, attr):
        field = self.get_field(fieldname)
        return self.get_last_attr(field, attr)
    def dir_get_first_attr(self, fieldname, attr):
        field = self.get_field(fieldname)
        return self.get_first_attr(field, attr)

    def save_config(self, filename):
        with open(filename, "w") as file:
            for w in self.words:
                if w == self.eol:
                    file.write(w)
                else:
                    file.write(w + " ")
    def set_field_attr(self, fieldname, attr, new_val):
        looking_for = '[' + fieldname + ']'
        start = 0
        found = False
        for w in self.words:
            start+=1
            if w == looking_for:
                found = True
                break
        if not found:
            raise BaseException("config_reader.py: set_field_attr: failed to find field " + looking_for)
        found = False
        if self.words[start] == self.eol:
            start+=1
        while start < len(self.words) and not is_field(self, self.words[start]):
            if self.words[start] == attr:
                found = True
                start+=1
                i = start
                erasing = False
                while i < len(self.words) and not is_field(self, self.words[i]) \
                        and self.words[i] != self.eol:
                    if i-start >= len(new_val):
                        erasing = True
                    if not erasing:
                        self.words[i] = new_val[i-start]
                    else:
                        self.words[i] = ""
                    i+=1
                while i-start < len(new_val):
                    self.words.insert(i, new_val[i-start])
                    i+=1
            start+=1

        if not found:
            raise BaseException("config_reader.py: set_field_attr: failed to find attr " + attr + " in field " + looking_for)
    def set_field(self, fieldname, new_field):
        looking_for = '[' + fieldname + ']'
        start = 0
        found = False
        for w in self.words:
            start+=1
            if w == looking_for:
                found = True
                break
        if not found:
            raise BaseException("config_reader.py: set_field_attr: failed to find field " + looking_for)
        i = start
        erasing = False
        while i < len(self.words) and not is_field(self, self.words[i]):
            if i-start >= len(new_field):
                erasing = True
            if not erasing:
                self.words[i] = new_field[i-start]
            else:
                self.words[i] = ""
            i+=1
        while i-start < len(new_field):
            self.words.insert(i, new_field[i-start])
            i+=1
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
    print(cfg.dir_get_attr("FIELD1", "MIN"))
    field = cfg.get_field("FIELD1")
    field[0] = "\n"
    field[1] = "this"
    field[2] = "is"
    field[3] = "a"
    field[4] = "test"
    field[5] = "\n"
    field.append("\n")
    field.append("test2")
    cfg.set_field("FIELD1", field)
    cfg.save_config("new.cfg")
