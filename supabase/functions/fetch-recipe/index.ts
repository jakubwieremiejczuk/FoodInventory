import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { DOMParser } from "https://deno.land/x/deno_dom@v0.1.38/deno-dom-wasm.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req: Request) => {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const { url } = await req.json();
    if (!url) {
      return new Response(JSON.stringify({ error: "Missing url" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // Fetch the recipe page
    const pageRes = await fetch(url, {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "pl-PL,pl;q=0.9",
      },
    });

    if (!pageRes.ok) {
      return new Response(
        JSON.stringify({ error: `Failed to fetch recipe: ${pageRes.status}` }),
        { status: 502, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const html = await pageRes.text();
    let title = "";
    let ingredients: string[] = [];

    // Strategy 1: JSON-LD schema.org/Recipe
    const jsonLdMatches = html.match(/<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi);
    if (jsonLdMatches) {
      for (const match of jsonLdMatches) {
        const jsonStr = match.replace(/<script[^>]*>/, "").replace(/<\/script>/, "").trim();
        try {
          let data = JSON.parse(jsonStr);

          // Handle @graph arrays
          if (data["@graph"]) {
            data = data["@graph"].find(
              (item: Record<string, string>) =>
                item["@type"] === "Recipe" ||
                (Array.isArray(item["@type"]) && item["@type"].includes("Recipe"))
            );
          }

          if (
            data &&
            (data["@type"] === "Recipe" ||
              (Array.isArray(data["@type"]) && data["@type"].includes("Recipe")))
          ) {
            title = data.name || "";
            if (Array.isArray(data.recipeIngredient)) {
              ingredients = data.recipeIngredient.map((s: string) => s.trim());
            }
            break;
          }
        } catch {
          // ignore invalid JSON
        }
      }
    }

    // Strategy 2: Parse HTML for ingredient lists
    if (ingredients.length === 0) {
      const doc = new DOMParser().parseFromString(html, "text/html");
      if (doc) {
        // Try to get title
        if (!title) {
          const h1 = doc.querySelector("h1");
          if (h1) title = h1.textContent.trim();
        }

        // Look for elements with ingredient-related classes or ids
        const selectors = [
          '[class*="ingredient"] li',
          '[class*="skladnik"] li',
          '[id*="ingredient"] li',
          '[id*="skladnik"] li',
          '.recipe-ingredients li',
          '.ingredients-list li',
        ];

        for (const sel of selectors) {
          const els = doc.querySelectorAll(sel);
          if (els.length > 0) {
            ingredients = Array.from(els).map((el) =>
              (el as unknown as { textContent: string }).textContent.trim()
            );
            break;
          }
        }

        // Fallback: look for <ul> after a header containing "składniki"
        if (ingredients.length === 0) {
          const headers = doc.querySelectorAll("h1, h2, h3, h4, h5, h6, strong, b");
          for (const h of headers) {
            const text = (h as unknown as { textContent: string }).textContent.toLowerCase();
            if (text.includes("składniki") || text.includes("skladniki")) {
              // Find next <ul> sibling
              let sibling = (h as unknown as { nextElementSibling: { tagName: string; querySelectorAll: (s: string) => NodeList } }).nextElementSibling;
              // Also check parent's next sibling
              if (!sibling || sibling.tagName !== "UL") {
                const parent = (h as unknown as { parentElement: { nextElementSibling: { tagName: string; querySelectorAll: (s: string) => NodeList } } }).parentElement;
                if (parent) sibling = parent.nextElementSibling;
              }
              if (sibling && sibling.tagName === "UL") {
                const lis = sibling.querySelectorAll("li");
                if (lis.length > 0) {
                  ingredients = Array.from(lis).map((el) =>
                    (el as unknown as { textContent: string }).textContent.trim()
                  );
                  break;
                }
              }
            }
          }
        }
      }
    }

    return new Response(
      JSON.stringify({ title, ingredients }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
