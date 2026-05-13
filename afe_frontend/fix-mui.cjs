const fs = require('fs');
const path = require('path');

function replaceInFiles(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            replaceInFiles(fullPath);
        } else if (fullPath.endsWith('.tsx') || fullPath.endsWith('.ts')) {
            let content = fs.readFileSync(fullPath, 'utf8');
            const originalContent = content;
            
            // 1. Remove empty props
            content = content.replace(/\s+(xs|sm|md|lg|xl)=\{\s*\}/g, '');
            
            // 2. Fix let color
            content = content.replace(/let\s+color\s*=\s*zentriaColors\.verde\.main;/g, 'let color: string = zentriaColors.verde.main;');
            content = content.replace(/let\s+color\s*:\s*["']#[0-9A-Fa-f]+["']\s*;/g, 'let color: string;');
            
            // 3. Fix cloneElement
            content = content.replace(/cloneElement\(icon\s+as\s+React\.ReactElement,\s*\{\s*sx:/g, 'cloneElement(icon as any, { sx:');
            content = content.replace(/cloneElement\(icon,\s*\{\s*sx:/g, 'cloneElement(icon as any, { sx:');
            
            // 4. Fix redundant type overlap isAdmin={(user?.rol === 'admin' || user?.rol === 'responsable') && user?.rol !== 'superadmin'}
            content = content.replace(/isAdmin=\{\(user\?\.rol === 'admin' \|\| user\?\.rol === 'responsable'\) && user\?\.rol !== 'superadmin'\}/g, "isAdmin={user?.rol === 'admin' || user?.rol === 'responsable'}");
            
            if (content !== originalContent) {
                fs.writeFileSync(fullPath, content);
                console.log('Updated: ' + fullPath);
            }
        }
    }
}

replaceInFiles(path.join(__dirname, 'src'));
