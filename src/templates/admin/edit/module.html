{% extends "app_base.html" %}
{% block title %}NettSS Editing {{module.name}}{% endblock %}
{% block extra_css %}
    <style>html { overflow-y: scroll !important; }</style>
{% endblock %}
{% block body %}
    <div style="text-align: center;">
        <h1 onclick="window.location.href = '/admin'"><div class="logo_name"><span style="color: #bc49db;">Nett</span><span>SS</span></div></h1>
    </div>
    <div style="padding: 8px 16px !important; margin: 8px 16px !important; border: 2px solid #50407040; border-radius: 8px;">
        <h1>Editing Module: {{module.name}}</h1>

        <form method="POST" style="display: inline;">
            <label>Name:</label>
            <input name="name" value="{{module.name}}"><br>
        
            <label>Description:</label>
            <textarea name="description">{{module.description}}</textarea><br>
        
            <label>Controls:</label>
            <textarea name="controls">{{module.controls}}</textarea><br>
        
            <label>Badges (comma-separated):</label>
            <input name="badges" value="{{ module.badges|join(', ') }}"><br>
        
            <label>Roblox Script Name:</label>
            <input name="roblox_name" value="{{module.roblox_name}}"><br>
        
            <label>Roblox Description:</label>
            <input name="roblox_description" value="{{module.roblox_description}}"><br>
        
            <label>Hidden?</label>
            <input type="checkbox" name="broken" {% if module.broken %}checked{% endif %}><br>
        
            <button type="submit" style="background:var(--nett)">Save JSON</button>
        </form>
        <button id="deleteBtn" style="background-color: red;">Delete</button>
        <button onclick="window.location.href = '/admin#sh'">Go back</button>

        <script>
            document.getElementById("deleteBtn").addEventListener("click", () => {
                Swal.fire({
                    title: "Delete Module?",
                    text: "This will permanently remove the module folder and all files.",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#d33",
                    cancelButtonColor: "#3085d6",
                    confirmButtonText: "Yes, delete it!"
                }).then((result) => {
                    if (result.isConfirmed) {
                        fetch("/admin/module/{{module_name}}/delete", {
                            method: "POST"
                        })
                        .then(r => r.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Deleted!", "Module has been removed.", "success")
                                  .then(() => window.location.href = "/admin#sh");
                            } else {
                                Swal.fire("Error", data.error || "Failed to delete module.", "error");
                            }
                        });
                    }
                });
            });
        </script>            

        <br>
        <br>
        <div class="module-editor">
            <label for="imageUpload">Module Image:</label>
            <img id="moduleImage" src="/api/module/{{module_name}}.png" alt="Module Image" style="max-width: 200px; display:block; margin-bottom: 10px;">
            <input type="file" id="imageUpload" accept="image/*">
        </div>
        <script>
            const imageInput = document.getElementById("imageUpload");
            const moduleImage = document.getElementById("moduleImage");
            
            moduleImage.addEventListener("click", () => imageInput.click());
            
            imageInput.addEventListener("change", async (event) => {
                const file = event.target.files[0];
                if (!file || !file.type.startsWith("image/")) return alert("Please select an image file.");
            
                const reader = new FileReader();
                reader.onload = e => moduleImage.src = e.target.result;
                reader.readAsDataURL(file);
            
                const formData = new FormData();
                formData.append("image", file);
            
                const response = await fetch("/admin/module/{{module_name}}/upload_image", {
                    method: "POST",
                    body: formData
                });
            
                if (!response.ok) alert("Failed to save image!");
            });
        </script>

        <br>
        {% if has_script %}
        <h2>script.luau</h2>
        <div id="container" style="width:100%; height:420px;"></div>

        <script src="/assets/vs/loader.js"></script>
        <script src="/assets/js/editor.js"></script>

        <script>
            function trySetText(value) {
                function trySet() {
                    try {
                        setText(value);
                    }
                    catch {
                        setTimeout(trySet, 100);
                    }
                }
                trySet()
            }
            fetch('/admin/module/{{module_name}}/script.luau')
              .then(r=>r.text())
              .then(t=>trySetText(t));
            
            function saveScript() {
                fetch("/admin/module/{{module_name}}/save_script", {
                    method:"POST",
                    headers:{"Content-Type":"application/x-www-form-urlencoded"},
                    body:"content="+encodeURIComponent(getText())
                }).then(()=>Swal.fire("Saved!"))
            }
        </script>

        <button onclick="saveScript()">Save Script</button>
        {% elif has_rbxmx %}
            <p>Current RBXMX: {{module.rbxmx}}</p>

            <form action="/admin/module/{{module_name}}/switch_to_script" method="POST" style="display:inline;">
                <button type="submit" style="background:var(--nett); margin-top:10px;">
                    Switch to script
                </button>
            </form>
        {% endif %}

        <form action="/admin/module/{{module_name}}/upload_rbxmx" method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".rbxmx">
            <button type="submit">Upload RBXMX</button>
        </form>

        {% if has_rbxmx %}
            <div>
                <label><b>Module ID:</b></label><br>
                <input type="number" id="id_value" value="{{ module_id if module_id else '0' }}" placeholder="Enter ID" style="width: 120px;">
            
                <button onclick="saveID()" style="margin-left: 10px; background: var(--nett);">
                    Save ID
                </button>
            </div>

            <script>
            function saveID() {
                const value = document.getElementById("id_value").value;
            
                fetch("/admin/module/{{module_name}}/save_id", {
                    method: "POST",
                    headers: {"Content-Type": "application/x-www-form-urlencoded"},
                    body: "id_value=" + encodeURIComponent(value)
                })
                .then(r => r.json())
                .then(data => {
                    if (data.success) Swal.fire("Saved!", "Module ID updated.", "success");
                    else Swal.fire("Error", data.error || "Failed saving ID", "error");
                });
            }
            </script>
        {% endif %}
    </div>
{% endblock %}
